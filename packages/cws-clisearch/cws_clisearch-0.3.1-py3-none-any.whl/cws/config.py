"""Package-wide config."""
import os
import yaml
from pathlib import Path


# Default user config
userconfig = {
    'default_provider': 'google',
    'provider': {
        'youtube': {
            'default_action': 'mpv'
        },
        'google': {
            'default_action': 'firefox'
        }
    }
}
tokensample = {
    'youtube': False,
    'google': False,
}


class Cfg():
    """CLI Web search config."""

    env = 'prod'
    token_filename = '.cws_tokens.yml'
    userconfig_filename = '.cws_config.yml'

    sample_path = Path(os.path.join(
        os.path.dirname(__file__), 'api_samples'
    ))
    int_provider_path = Path(os.path.join(
        os.path.dirname(__file__), 'provider'
    ))

    def __init__(self):
        """Construct the config."""
        self.token_file = self.__get_config_file(self.token_filename)
        self.tokens = self.__load_file(self.token_file, tokensample)

        self.userconfig_file = self.__get_config_file(self.userconfig_filename)
        self.userconfig = self.__load_file(self.userconfig_file, userconfig)

        self.provider_yamls = self.__get_providers()

    def __get_providers(self):
        """Gather provider yamls from filesystem as a list.

        Todo:
            * Load providers from user locations
        """
        providers = {}

        for node in self.int_provider_path.iterdir():
            if '.yml' in str(node):
                providers[str(node.stem)] = str(node)

        return providers

    def __load_file(self, conf_file, sample):
        """Parse the config file to a dict.

        By merging it with the defined sample.

        Args:
            conf_file: The config file Path to load
            sample: The sample to merge with

        Returns:
            dict: A parsed config file
        """
        if not conf_file:
            return sample

        with open(conf_file, 'r') as file:
            try:
                final = sample.copy()
                final.update(yaml.safe_load(file))
                return final
            except yaml.YAMLError:
                return sample
            except TypeError:
                return sample

    def __get_config_file(self, name):
        """Try fetching a config file from filesystem.

        Looks in both XDG home and general HOME.

        Args:
            name: The name of the file to search for.

        Returns:
            Path: The path or False
        """
        home = os.environ.get('HOME')
        if home:
            home_cfg = Path(home) / name
            if home_cfg.is_file():
                return home_cfg

        xdg_conf_home = os.environ.get('XDG_CONFIG_HOME')
        if xdg_conf_home:
            xdg_cfg = Path(xdg_conf_home) / 'cws' / name
            if xdg_cfg.is_file():
                return xdg_cfg

        return False


cfg = Cfg()
