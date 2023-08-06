"""
This module contains a tool functions used to create a new project.
"""

import shutil
import glob
import os
from multiprocessing import Lock, Process, Queue, Manager, cpu_count

from .constants import (
    CWD,
    DEFAULT_DATA_DIR,
    USER_PATH,
    MODULE_DATA_PATH,
    WEATHER_FILES,
)


def _find_files_oswalk(root, templates_search_dir, search=None):
    """
    Finds all files via os.walk.

    Args:
        root (str): Root path.
        templates_search_dir (str): Dictionary of the templates.
        search ([type], optional): Search index. Defaults to None.

    Yields:
        file, root, section, basefile, exists
    """
    for file in glob.glob(os.path.join(root, templates_search_dir, "**/*.*"), recursive=True):
        exists = False
        section = ""
        basefile = os.path.basename(file)
        inbetween = file[len(root) + 1: -len(basefile) - 1].split(os.sep)
        newsection = inbetween[:]
        if search is not None:
            if search in inbetween:
                exists = True
                newsection.remove(search)
            if templates_search_dir in inbetween:
                newsection.remove(templates_search_dir)
        if newsection:
            section = os.path.join(*newsection)
        yield file, root, section, basefile, exists


def copy_to_user_data_dir(location=None):
    """
    Copies files to user data directory.

    Args:
        location (str, optional): Location to which files should be copied. Defaults to None.
    """
    user_dir = location or USER_PATH or DEFAULT_DATA_DIR
    os.makedirs(user_dir, exist_ok=True)
    PKG_DATA_FILES = glob.glob(os.path.join(MODULE_DATA_PATH, "*.*"))
    for file in PKG_DATA_FILES:
        basefile = os.path.basename(file)
        if basefile in WEATHER_FILES.keys():
            rest = file.rsplit(MODULE_DATA_PATH)[-1][1:]
            base = rest.rsplit(basefile)[0][:-1]
            destpath = os.path.join(user_dir, base, WEATHER_FILES[basefile])
            if not os.path.exists(destpath):
                print(destpath)
                os.makedirs(os.path.split(destpath)[0], exist_ok=True)
                shutil.copyfile(file, destpath)
        else:
            rest = file.rsplit(MODULE_DATA_PATH)[-1][1:]
            destpath = os.path.join(user_dir, rest)
            if not os.path.exists(destpath):
                print(destpath)
                os.makedirs(os.path.split(destpath)[0], exist_ok=True)
                shutil.copyfile(file, destpath)


def create_project(project_name, template):
    """
    Creates project based on selected template and copies these files.

    Args:
        project_name (str): Chosen project name.
        template (str): Chosen template.

    Raises:
        Exception: Template arguments not valid.
        Exception: Chosen folder does not exist.
    """
    template_check = ["base", "eg1", "eg2", "eg3"]
    if template in template_check:
        pass
    else:
        raise Exception(
            f"--template argument '{template}' not in {' '.join(template_check)}"
        )

    template_dir_path = os.path.join(MODULE_DATA_PATH, template)
    if not os.path.exists(template_dir_path):
        raise Exception(
            f"Directory '{template_dir_path}' does not exist. Make sure you call copy_to_user_data_dir function first"
        )

    print(f"Copy files from {template_dir_path}")
    for file, _, section, basefile, _ in _find_files_oswalk(template_dir_path, ""):
        destination_file_abspath = os.path.join(CWD, project_name, section, basefile)
        os.makedirs(os.path.split(destination_file_abspath)[0], exist_ok=True)
        shutil.copyfile(file, destination_file_abspath)
        print(f"   {destination_file_abspath}")
    print("Done!")

def check_for_new_function_name(attribute_error_name):
    new_names = {
        'ChooseChargingPoint': '_choose_charging_point',
        'ChooseChargingPointFast': '_choose_charging_point_fast',
        'drawing_soc': '_drawing_soc',
        'fill_rows': '_fill_rows',
        'initial_conf': '_initial_conf',
        'loadSettingDriving': '_load_setting_driving',
        'save_profile': 'save_profile',
        'setBatteryRules': '_set_battery_rules',
        'setScenario': 'set_scenario',
        'setVehicleFeature': '_set_vehicle_feature',
        'soc': '_soc',
        'testing_soc': '_testing_soc',

        'A2BatPoint': '_A2BatPoint',
        'balanced': '_balanced',
        'changeBatteryCapacity': 'x',
        'check_success': '_check_success',
        'immediate': '_immediate',
        'loadScenario': 'load_scenario',
        'setSubScenario': 'set_sub_scenario',

        'load_specs': '_load_specs',

        'cop_and_target_temp': '_cop_and_target_temp',
        'ev_par_test': '_ev_par_test',
        'loadSettingMobility': 'load_setting_mobility',

        'select_driving_cycle_index': '_select_driving_cycle_index',
        'get_index_speed': '_get_index_speed',

        'check': '_check',
        'layers_name': '_layers_name',
        'makearrays': '_makearrays',
        'zones_name': '_zones_name',

        'get_codes': '_get_codes',
        'get_efficiency': '_get_efficiency',
        'load_file': '_load_file',

        'frontal_area': '_frontal_area',
        'PMR': '_pmr',

        'airDensityFromIdealGasLaw': 'air_density_from_ideal_gas_law',
        'calcDewPoint': 'calc_dew_point',
        'calcDryAirPartialPressure': 'calc_dry_air_partial_pressure',
        'calcRelHumidity': 'calc_rel_humidity',
        'calcVaporPressure': 'calc_vapor_pressure',
        'humidairDensity': 'humidair_density',

        'loadfilesBatch': 'loadfiles_batch',
        'clean': '_clean',
        'group_trips_week': '_group_trips_week',
        'logging_meetcond': '_logging_meetcond',
        'MeetAllConditions': '_meet_all_conditions',
        'select_tour': '_select_tour',
        'setParams': 'set_params',
        'setStats': 'set_stats',
        'setRules': 'set_rules',
    }
    if attribute_error_name in new_names.keys():
        raise AttributeError(f'{attribute_error_name} does not exist. Note: We changed the attribute names from camelCase '
                        f'to snake_case. \n The new attribute name for {attribute_error_name} is {new_names[attribute_error_name]}.')
    else:
        raise AttributeError(f'{attribute_error_name} does not exist. Note: We changed the attribute names from camelCase '
                        f'to snake_case. \n You may have to adapt your attributes.')


def parallelize(function=None, inputdict: dict = None, nr_workers=1, **kargs):
    """
    Parallelize function to run program faster.
    The queue contains tuples of keys and objects, the function must be consistent when getting data from queue.

    Args:
        function (function, optional): Function that is to be parallelized. Defaults to None.
        inputdict (dict, optional): Contains numbered keys and as value any object. Defaults to None.
        nr_workers (int, optional): Number of workers, so their tasks can run parallel. Defaults to 1.

    Returns:
        dict: Dictionary the given functions creates.
    """
    total_cpu = cpu_count()
    print(f"Workers: {nr_workers} of {total_cpu}")
    if nr_workers > total_cpu:
        nr_workers = total_cpu
        print(f"Workers: {nr_workers}")
    with Manager() as manager:
        dc = manager.dict()
        queue = Queue()
        for key, item in inputdict.items():
            queue.put((key, item))
        queue_lock = Lock()
        processes = {}
        for i in range(nr_workers):
            if kargs:
                processes[i] = Process(target=parallel_func,
                                       args=(
                                           dc,
                                           queue,
                                           queue_lock,
                                           function,
                                           kargs,
                                       ))
            else:
                processes[i] = Process(target=parallel_func,
                                       args=(
                                           dc,
                                           queue,
                                           queue_lock,
                                           function,
                                       ))
            processes[i].start()
        for i in range(nr_workers):
            processes[i].join()
        outputdict = dict(dc)
    return outputdict


def parallel_func(dc, queue=None, queue_lock=None, function=None, kargs={}):
    """
    #TODO DOCSTRING

    Args:
        dc ([type]): [description]
        queue ([type], optional): [description]. Defaults to None.
        queue_lock ([type], optional): [description]. Defaults to None.
        function ([type], optional): [description]. Defaults to None.
        kargs (dict, optional): [description]. Defaults to {}.

    Returns:
        [type]: [description]
    """

    while True:
        queue_lock.acquire()
        if queue.empty():
            queue_lock.release()
            return None
        key, item = queue.get()
        queue_lock.release()
        obj = function(**item, **kargs)
        dc[key] = obj
