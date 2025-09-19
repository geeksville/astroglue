

import os
import shutil
import textwrap
from glob import glob
import tempfile
import subprocess
import re

import logging
logger = logging.getLogger(__name__)

target="NGC 281"

# paths of the form
# /images/from_astroboy/NGC 281/2025-09-16/FLAT/2025-09-17_00-00-29_HaOiii_-9.90_6.22s_0002.fits
# /images/from_astroboy/NGC 281/2025-09-16/LIGHT/2025-09-17_00-43-32_SiiOiii_-9.90_120.00s_0006.fits
repo="/images/from_astroboy"
siril_work="/images/siril_new"
process_dir=f"{siril_work}/process"

# directories of the form /images/from_astroboy/masters-raw/2025-09-09/BIAS/2025-09-09_20-33-19_Dark_-9.70_0.00s_0030.fits
masters_raw="/images/from_astroboy/masters-raw"

# High value preprocecssed outputs
preprocessed="/images/preprocessed"
masters=preprocessed+"/masters"
targets=preprocessed+"/targets"

def siril_run(cwd: str, commands: str) -> None:
    """Executes Siril with a script of commands in a given working directory."""
    script_content = textwrap.dedent(f"""
        requires 1.4.0-beta3
        {commands}
        """)
    
    # The `-s -` arguments tell Siril to run in script mode and read commands from stdin.
    cmd = f"org.siril.Siril -d {cwd} -s -"

    logger.debug(f"Running Siril command in {cwd}: {commands}")
    result = subprocess.run(
        cmd, 
        input=script_content, 
        shell=True, 
        capture_output=True, 
        text=True, 
        cwd=cwd
    )

    if result.stdout:
        logger.debug(f"Siril output:\n")
        for line in result.stdout.splitlines():
            logger.debug(line)

    if result.stderr:
        logger.warning(f"Siril error message:")
        for line in result.stderr.splitlines():
            logger.warning(line)

    if result.returncode != 0:
        logger.error(f"Siril command failed with exit code {result.returncode}!")
        result.check_returncode()  # Child process returned an error code
    else:
        logger.info("Siril command successful.")



def siril_run_in_temp_dir(input_files: list[str], commands: str) -> None:
    # Create a temporary directory for processing
    temp_dir = tempfile.mkdtemp(prefix="siril_")

    # Create symbolic links for all input files in the temp directory
    for f in input_files:
        os.symlink(os.path.abspath(str(f)), os.path.join(temp_dir, os.path.basename(str(f))))

    # Run Siril commands in the temporary directory
    try:
        logger.info(f"Running Siril in temporary directory: {temp_dir}, cmds {commands}")
        siril_run(temp_dir, commands)
    finally:
        shutil.rmtree(temp_dir)
        pass  # Keep temp dir for debugging


def get_master_bias_path() -> str:
    date = "2025-09-09"  # FIXME - later find latest date with bias frames
    output = f"{masters}/biases/{date}_stacked.fits"

    if os.path.exists(output):
        logger.info(f"Using existing master bias: {output}")
        return output
    else:
        frames = glob(f"{masters_raw}/{date}/BIAS/{date}_*.fit*")

        siril_run_in_temp_dir(frames, textwrap.dedent(f"""
            # Convert Bias Frames to .fit files
            link bias -out={process_dir}
            cd {process_dir}

            # Stack Bias Frames to bias_stacked.fit
            stack bias rej 3 3 -nonorm -out={output}
            """))
        
        return output
    

def strip_extension(path: str) -> str:
    """Removes the file extension from a given path."""
    return os.path.splitext(path)[0]

def find_frames(target: str, sessionid: str, sessionconfig: str, frametype: str) -> list[str]:
    """
    Finds all frames of a given type (e.g., 'FLAT', 'LIGHT') for a specific target,
    session, and filter configuration.
    """
    frames_path = f"{repo}/{target}/{sessionid}/{frametype}/*_{sessionconfig}_*.fit*"
    frames = glob(frames_path)
    if not frames:
        logger.error(f"No {frametype} frames found for session {sessionid}, config {sessionconfig} at {frames_path}")
        raise FileNotFoundError(f"No {frametype} frames found for {sessionid}/{sessionconfig}")
    return frames


def get_flat_path(sessionid: str, sessionconfig: str, bias: str) -> str:
    """
    Finds or creates a master flat for a given session and filter configuration.
    The master flat is calibrated with the provided master bias.
    """
    # Output path for the master flat, specific to the session and config
    output_base = f"flat_s{sessionid}_c{sessionconfig}"
    output = f"{process_dir}/{output_base}.fits"

    # If the master flat already exists, skip creation and return its path
    if os.path.exists(output):
        logger.info(f"Using existing master flat: {output}")
        return output
    else:
        logger.info(f"Creating master flat for session {sessionid}, config {sessionconfig} -> {output}")
        os.makedirs(process_dir, exist_ok=True)

        # Find all raw flat frames for the given session and filter (sessionconfig)
        frames = find_frames(target, sessionid, sessionconfig, "FLAT")

        # Siril commands to create the master flat.
        # Paths for bias and output must be absolute since Siril runs in a temp directory.
        commands = textwrap.dedent(f"""
            # Create a sequence from the raw flat frames
            link {output_base} -out={process_dir}
            cd {process_dir}
            # Calibrate the flat frames using the master bias
            calibrate {output_base} -bias={strip_extension(bias)}
            # Stack the pre-processed (calibrated) flat frames
            stack pp_{output_base} rej 3 3 -norm=mul -out={output}
            """)
        siril_run_in_temp_dir(frames, commands)
        return output

def make_bkg_pp_light(sessionid: str, sessionconfig: str, bias: str, flat: str):
    """
    Calibrates light frames for a given session and filter configuration.
    This creates a pre-processed (pp_) sequence in the process directory.
    """
    light_base = f"light_s{sessionid}_c{sessionconfig}"
    output_base = f"Ha_bkg_pp_{light_base}"

    # If the calibrated sequence already exists, skip creation
    if glob(f"{process_dir}/{output_base}_.seq"):
        logger.info(f"Using existing calibrated light sequence: {output_base}")
        return output_base

    logger.info(f"Creating calibrated light sequence for session {sessionid}, config {sessionconfig} -> {output_base}")
    os.makedirs(process_dir, exist_ok=True)

    # Find all raw light frames for the given session and filter
    frames = find_frames(target, sessionid, sessionconfig, "LIGHT")

    # Siril commands to calibrate the light frames.
    # This runs in a temp dir with symlinks to raw files, but cds into process_dir to work.
    commands = textwrap.dedent(f"""
        # Create a sequence from the raw light frames, seq file goes to process_dir
        link {light_base} -out={process_dir}
        cd {process_dir}

        # Calibrate the light frames using master bias and flat
        calibrate {light_base} -bias={strip_extension(bias)} -flat={strip_extension(flat)} -cfa -equalize_cfa

        # Remove background gradient on a per-frame basis (generates bkg_pp_{light_base}.seq)
        seqsubsky pp_{light_base} 1

        # FIXME only do this step for duo filters (refactor to share common light processing function)
        seqextract_HaOIII bkg_pp_{light_base} -resample=ha
        """)
    siril_run_in_temp_dir(frames, commands)

def make_stacked(sessionconfig: str, variant: str, output_file: str):
    """
    Registers and stacks all pre-processed light frames for a given filter configuration
    across all sessions.
    """
    # The sequence name for all frames of this variant and config, across all sessions
    # e.g. Ha_bkg_pp_light_cHaOiii
    merged_seq_base = f"{variant}_bkg_pp_light"

    # Absolute path for the output stacked file
    stacked_output_path = glob(f"{process_dir}/{output_file}.fit*")

    if stacked_output_path:
        logger.info(f"Using existing stacked file: {stacked_output_path}")
    else:
        # Merge all frames (from multiple sessions and configs) use those for stacking
        frames = glob(f"{process_dir}/{variant}_bkg_pp_light_s*_c{sessionconfig}_*.fit*")

        logger.info(f"Registering and stacking {len(frames)} frames for {sessionconfig}/{variant} -> {stacked_output_path}")

        # Siril commands for registration and stacking. We run this in process_dir.
        commands = textwrap.dedent(f"""
            link {merged_seq_base} -out={process_dir}
            cd {process_dir}

            register {merged_seq_base}
            stack r_{merged_seq_base} rej g 0.3 0.05 -filter-wfwhm=3k -norm=addscale -output_norm -32b -out={output_file}
            
            # and flip if required
            mirrorx_single {output_file}
            """)
        
        siril_run_in_temp_dir(frames, commands)

def make_renormalize():
    """
    Aligns the stacked images (Sii, Ha, OIII) and renormalizes Sii and OIII
    to match the flux of the Ha channel.
    """
    logger.info("Aligning and renormalizing stacked images.")

    # Define file basenames for the stacked images created in the 'process' directory
    sii_base = "results_00001"
    ha_base = "results_00002"
    oiii_base = "results_00003"

    # Define final output paths. The 'results' directory is a symlink in the work dir.
    results_dir = f"{targets}/{target}"
    os.makedirs(results_dir, exist_ok=True)
    
    ha_final_path = f"{results_dir}/stacked_Ha.fits"
    sii_final_path = f"{results_dir}/stacked_Sii.fits"
    oiii_final_path = f"{results_dir}/stacked_OIII.fits"

    # Check if final files already exist to allow resuming
    if all(os.path.exists(f) for f in [ha_final_path, sii_final_path, oiii_final_path]):
        logger.info("Renormalized files already exist, skipping.")
        return

    # Basenames for registered files (output of 'register' command)
    r_sii = f"r_{sii_base}"
    r_ha = f"r_{ha_base}"
    r_oiii = f"r_{oiii_base}"

    # Pixel math formula for renormalization.
    # It matches the median and spread (MAD) of a channel to a reference channel (Ha).
    # Formula: new = old * (MAD(ref)/MAD(old)) - (MAD(ref)/MAD(old)) * MEDIAN(old) + MEDIAN(ref)
    pm_oiii = f'"${r_oiii}$*mad(${r_ha}$)/mad(${r_oiii}$)-mad(${r_ha}$)/mad(${r_oiii}$)*median(${r_oiii}$)+median(${r_ha}$)"'
    pm_sii = f'"${r_sii}$*mad(${r_ha}$)/mad(${r_sii}$)-mad(${r_ha}$)/mad(${r_sii}$)*median(${r_sii}$)+median(${r_ha}$)"'

    # Siril commands to be executed in the 'process' directory
    commands = textwrap.dedent(f"""
        register results -transf=shift -interp=none
        pm {pm_oiii}
        save "{oiii_final_path}"
        pm {pm_sii}
        save "{sii_final_path}"
        load {r_ha}
        save "{ha_final_path}"
        """)

    siril_run(process_dir, commands)
    logger.info(f"Saved final renormalized images to {results_dir}")

def get_sessions(target: str) -> list[str]:
    """
    Finds session directories for a given target.
    A session directory is expected to be a direct subdirectory of the target's path,
    with a name in the format YYYY-MM-DD.
    Returns a list of directory names (e.g., ['2025-09-16']).
    """
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    base_path = f"{repo}/{target}"
    
    if not os.path.isdir(base_path):
        logger.warning(f"Target directory not found: {base_path}")
        return []

    return [entry.name for entry in os.scandir(base_path)
            if entry.is_dir() and date_pattern.match(entry.name)]

def get_session_configs(sessionid: str) -> list[str]:
    """
    Finds filter configurations for a given session by inspecting FLAT filenames.

    It looks for files in the session's FLAT directory and parses the filter name
    from filenames like 'DATE_TIME_FILTER_...'.

    Args:
        sessionid (str): The ID of the session, typically a date like '2025-09-16'.

    Returns:
        list[str]: A list of unique filter names found (e.g., ['HaOiii', 'SiiOiii']).
    """
    flat_dir = f"{repo}/{target}/{sessionid}/FLAT"
    if not os.path.isdir(flat_dir):
        logger.warning(f"FLAT directory not found for session {sessionid} at {flat_dir}")
        return []

    # Regex to capture the filter name (3rd component) from filenames like:
    # 2025-09-17_00-00-13_HaOiii_-10.00_6.22s_0000.fits
    filter_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_(?P<filter>[^_]+)_.+\.fits?$")

    # Use a set comprehension to efficiently find unique filter names from filenames.
    filters = {match.group('filter') for f in os.listdir(flat_dir) if (match := filter_pattern.match(f))}

    found_filters = sorted(list(filters))
    logger.info(f"Found filters for session {sessionid}: {found_filters}")
    return found_filters
"""
notes:

inputs:
targets have session (listed by sessionid(date) typically one per night)
each session has a sessionconfig (different filter names)
each session config has flats and lights

masters_raw:
    <date>/BIAS/*.fits

outputs:
  masters:
    bias

process: (one big flat directory)
  _s<sessionid>_c<sessionconfig>: (THIS IS A SUFFIX ADDED TO EACH BASENAME for the following 'session/config' specific files)
    flat.fits (stacked calibrated flat for this session and config)
    pp_light.seq (= calibrated lights)
    bkg_pp_light.seq (= calibrated and linear background corrected lights)

    Ha_bkg_pp_light.seq (seq extract by color)
    Oiii_bkg_pp_light.seq (seq extract by color)    

  _c<sessionconfig>: (THIS IS A SUFFIX ADDED TO EACH BASENAME for the following files - accross all sessions, but per config)
    Ha_bkg_pp_light.seq (merged from all sessions)
    r_Ha_bkg_pp_light.seq (registered)  
    stacked_r_Ha_bkg_pp_light.fit (stacked)
    flipped_00001.fit (flipped for Ha)

    Oiii_bkg_pp_light.seq (merged from all sessions)
    r_Oiii_bkg_pp_light.seq (registered)
    stacked_r_Oiii_bkg_pp_light.fit (stacked)
    flipped_00002.fit (flipped for Oiii)

    FIXME - later add 03 for Sii, and stack the two Oiii variants together
    r_Sii_bkg_pp_light.seq (registered)
    stacked_r_Sii_bkg_pp_light.fit (stacked)
    flipped_00003.fit (flipped for Sii)

    r_flipped.seq (flipped and registered)

preprocessed: (high value output files)
    result_Ha.fit
    result_Oiii.fit

later:
    result_Sii.fit
    graxpert bkg removal
    result_HaOiiiSii.fit (combined Ha, Oiii, Sii via pixel math post graxpert)
    with and without stars

FIXME:
  add caching of masters and flats in TBD directories
"""

def main() -> None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s - %(message)s')
    logger.info("Starting processing")

    # find/create master bias as needed
    bias = get_master_bias_path()

    sessions = get_sessions(target)
    all_configs = set()
    for sessionid in sessions:
        for sessionconfig in get_session_configs(sessionid):
            all_configs.add(sessionconfig)
            # find/create flat.fits as needed
            flat = get_flat_path(sessionid, sessionconfig, bias)
            make_bkg_pp_light(sessionid, sessionconfig, bias, flat)
    
    logger.info(f"All session configs: {all_configs}")
    variants = ["Ha", "OIII"] # FIXME: solve capitalization issues and work with single or dual Duo filter
    # for sessionconfig in all_configs:
    #for i, variant in enumerate(variants):

    # red output channel - from the SiiOiii filter Sii is on the 672nm red channel (mistakenly called Ha by siril)
    make_stacked("SiiOiii", "Ha", f"results_00001") 

    # green output channel - from the HaOiii filter Ha is on the 656nm red channel
    make_stacked("HaOiii", "Ha", f"results_00002")

    # blue output channel - both filters have Oiii on the 500nm blue channel.  Note the case here is uppercase to match siril output
    make_stacked("*", "OIII", f"results_00003")

    # There might be an old/state autogenerated .seq file, delete it so it doesn't confuse renormalize
    results_seq_path = f"{process_dir}/results_.seq"
    if os.path.exists(results_seq_path):
        os.remove(results_seq_path)

    make_renormalize()
    # make merged


if __name__ == "__main__":
    main()