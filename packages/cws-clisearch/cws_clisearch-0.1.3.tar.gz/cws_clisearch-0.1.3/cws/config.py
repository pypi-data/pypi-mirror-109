"""Package-wide config."""
import os
import yaml
from pathlib import Path


# Default user config
userconfig = {
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
    sample_path = Path(os.path.join(
        os.path.dirname(__file__), 'api_samples'))

    def __init__(self):
        """Construct the config."""
        self.token_filename = '.cws_tokens.yml'
        self.token_file = self.__get_config_file(self.token_filename)
        self.tokens = self.__load_token_file()

        self.userconfig_filename = '.cws_config.yml'
        self.userconfig_file = self.__get_config_file(self.userconfig_filename)
        self.userconfig = self.__load_userconfig_file()

    def __load_token_file(self):
        """Parse the config file to a dict."""
        if not self.token_file:
            return tokensample

        with open(self.token_file, 'r') as file:
            try:
                tokens = tokensample.copy()
                tokens.update(yaml.safe_load(file))
                return tokens
            except yaml.YAMLError:
                return tokensample
            except TypeError:
                return tokensample

    def __load_userconfig_file(self):
        """Parse the userconfig file."""
        if not self.userconfig_file:
            return userconfig

        with open(self.userconfig_file, 'r') as file:
            try:
                custom_conf = userconfig.copy()
                custom_conf.update(yaml.safe_load(file))
                return custom_conf
            except yaml.YAMLError:
                return userconfig
            except TypeError:
                return userconfig

    def __get_config_file(self, name):
        """Try fetching a config file from filesystem."""
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
