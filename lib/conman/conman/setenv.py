from omegaconf import DictConfig


def replace_env_values(
    d: DictConfig,
    env: str,
) -> None:
    """Function that mutates the configuration object from Hydra and sets the environment
    Used in conjunction with Hydra multiple configs with config groups
    https://hydra.cc/docs/patterns/select_multiple_configs_from_config_group/

    Example:
      When used from a directory from repo root as ./dir/dir/
      initialize(version_base=None, config_path="../../conf")
      cfg = compose(config_name="config")

    Args:
        d (DictConfig): a hydra configuration file
        env (str): environment variable
    """
    for k, v in d.items():
        if isinstance(v, DictConfig):
            replace_env_values(v, env)
        elif isinstance(v, str):
            d[k] = v.replace("<env>", env)
