import argparse
import logging
from pkg_resources import get_distribution
import sys

from . import blobs, email, hashes, hostname, ip, url


logger = logging.getLogger(name=__name__)


REFANGING_MODULES = [url, email, hostname, ip]


def extract_all(text, refang=False, blob_text_depth=1, **blob_decode_kwargs):
	for module in REFANGING_MODULES:
		yield from module.extract(text=text, refang=refang)

	yield from hashes.extract(text=text)
	for blob_text in blobs.extract_text(
			text=text, depth=blob_text_depth, **blob_decode_kwargs):
		yield blob_text
		yield from extract_all(
			text=blob_text, refang=refang, blob_text_depth=0)


def main():
	package_name, *_ = __name__.split('.', 1)
	package_version = get_distribution(package_name).version
	root_parser = argparse.ArgumentParser(
		description='Indicator of Compromise (IOC) Detection')

	root_parser.add_argument(
		'-V', '--version',
		action='version',
		version=f'%(prog)s {package_version}',
	)
	root_parser.add_argument('-l', '--log-level', default='INFO')
	root_parser.add_argument('-r', '--refang', action='store_true')

	root_parser.set_defaults(function=extract_all)

	subparsers = root_parser.add_subparsers()
	
	all_parser = subparsers.add_parser('all')
	all_parser.set_defaults(function=extract_all)

	blobs_parser = subparsers.add_parser('blobs')
	blobs_parser.set_defaults(function=blobs.extract)

	email_parser = subparsers.add_parser('email')
	email_parser.set_defaults(function=email.extract)

	hashes_parser = subparsers.add_parser('hashes')
	hashes_parser.set_defaults(function=hashes.extract)

	hostname_parser = subparsers.add_parser('hostname')
	hostname_parser.set_defaults(function=hostname.extract)

	ip_parser = subparsers.add_parser('ip')
	ip_parser.set_defaults(function=ip.extract)

	url_parser = subparsers.add_parser('url')
	url_parser.set_defaults(function=url.extract)

	secrets_parser = subparsers.add_parser('secrets')
	secrets_parser.set_defaults(function=blobs.extract_text)

	namespace = root_parser.parse_args(sys.argv[1:])
	arguments = vars(namespace)

	log_level = arguments.pop('log_level')
	logging.basicConfig(level=log_level.upper())
	logger.debug('parsed args: %r', namespace)

	in_file = sys.stdin
	out_file = sys.stdout
	command_function = namespace.function
	if command_function is hashes.extract:
		out_values = hashes.extract(in_file.read())
	elif command_function is blobs.extract_text:
		out_values = blobs.extract_text(in_file.read())
	else:
		out_values = command_function(in_file.read(), refang=namespace.refang)

	out_file.writelines(f'{v}\n' for v in out_values)
