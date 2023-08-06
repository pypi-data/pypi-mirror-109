
#   Copyright 2021 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
#
import argparse
import logging
import sys

import tripleo_yum_config.exceptions as exc
import tripleo_yum_config.yum_config as cfg


def main():
    cfg.TripleOYumConfig.load_logging()

    # Common parser argument for all commands
    common_parse = argparse.ArgumentParser(add_help=False)
    common_parse.add_argument(
        '--config-file-path',
        dest='config_file_path',
        help=('set the absolute file path of the configuration file to be '
              'updated')
    )

    repo_args_parser = argparse.ArgumentParser(add_help=False)
    repo_args_parser.add_argument(
        'name',
        help='name of the repo or module to be updated'
    )
    parser_enable_group = repo_args_parser.add_mutually_exclusive_group()
    parser_enable_group.add_argument(
        '--enable',
        action='store_true',
        dest='enable',
        default=None,
        help='enable a yum repo or module'
    )
    parser_enable_group.add_argument(
        '--disable',
        action='store_false',
        dest='enable',
        default=None,
        help='disable a yum repo or module'
    )
    repo_args_parser.add_argument(
        '--config-dir-path',
        dest='config_dir_path',
        help=(
            'set the absolute directory path that holds all repo or module '
            'configuration files')
    )

    options_parse = argparse.ArgumentParser(add_help=False)
    options_parse.add_argument(
        '--set-opts',
        dest='set_opts',
        nargs='+',
        help='sets config options as key=value pairs for a specific '
             'configuration file'
    )

    main_parser = argparse.ArgumentParser()
    main_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='enable verbose log level for debugging',
    )
    subparsers = main_parser.add_subparsers(dest='command')

    subparsers.add_parser(
        'repo',
        parents=[common_parse, repo_args_parser, options_parse],
        help='updates a yum repository options'
    )
    subparsers.add_parser(
        'module',
        parents=[common_parse, repo_args_parser, options_parse],
        help='updates yum module options'
    )
    subparsers.add_parser(
        'global',
        parents=[common_parse, options_parse],
        help='updates global yum configuration options'
    )

    args = main_parser.parse_args()
    if args.command is None:
        main_parser.print_help()
        sys.exit(2)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('Logging level set to DEBUG')

    set_dict = {}
    if args.set_opts:
        for opt in args.set_opts:
            try:
                k, v = opt.split('=')
            except ValueError:
                msg = 'Set options must be provided as "key=value" pairs'
                raise exc.TripleOYumConfigInvalidOption(error_msg=msg)
            set_dict[k] = v

    if args.command == 'repo':
        config_obj = cfg.TripleOYumRepoConfig(
            file_path=args.config_file_path,
            dir_path=args.config_dir_path)

        config_obj.update_section(args.name, set_dict, enable=args.enable)

    elif args.command == 'module':
        config_obj = cfg.TripleOYumModuleConfig(
            file_path=args.config_file_path,
            dir_path=args.config_dir_path)

        config_obj.update_section(args.name, set_dict, enable=args.enable)

    elif args.command == 'global':
        config_obj = cfg.TripleOYumGlobalConfig(
            file_path=args.config_file_path)

        config_obj.update_section('main', set_dict)


def cli_entrypoint():
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        logging.info("Exiting on user interrupt")
        raise


if __name__ == "__main__":
    main()
