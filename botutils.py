import yaml
import logging


def set_logging(log_level=logging.INFO):
    """
    Create a logger.
    :param log_level: Log level to user. See logging module for its levels
    :return: Created Logger
    """
    logging.basicConfig(level=log_level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)


# Read the environment file
def get_environment():
    """
    Get environment variables.
    :return: Dictionary with environment variables
    :raise OSError:
    """
    with open('env.yaml', 'r') as f:
        env_dict = yaml.load(f, Loader=yaml.FullLoader)
    return env_dict


def check_env_requirements(env_dict):
    """
    Check if environment dictionary has all minimum required variables.
    :param env_dict:
    :return: Empty string if variables are ok. String with errors description otherwise
    """
    errors_description = ""
    if not env_dict or 'SECRET_BOT_TOKEN' not in env_dict:
        errors_description += "Be sure to have the \"SECRET_BOT_TOKEN\" value set in the \"env.yaml\"\n"
    if not env_dict or 'DB_USERNAME' not in env_dict:
        errors_description += "Be sure to have the \"DB_USERNAME\" value set in the \"env.yaml\" to correctly connect to the DB\n"
    if not env_dict or 'DB_PASSWORD' not in env_dict:
        errors_description += "Be sure to have the \"DB_PASSWORD\" value set in the \"env.yaml\" to correctly connect to the DB\n"
    return errors_description
