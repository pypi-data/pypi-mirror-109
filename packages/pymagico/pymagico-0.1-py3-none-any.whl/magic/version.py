from cerver.utils.log import LOG_TYPE_NONE, cerver_log_both

from .lib import lib

PYMAGIC_VERSION = "0.1".encode ('utf-8')
PYMAGIC_VERSION_NAME = "Version 0.1".encode ('utf-8')
PYMAGIC_VERSION_DATE = "09/06/2021".encode ('utf-8')
PYMAGIC_VERSION_TIME = "08:35 CST".encode ('utf-8')
PYMAGIC_VERSION_AUTHOR = "Erick Salas".encode ('utf-8')

magic_version_print_full = lib.magic_version_print_full
magic_version_print_version_id = lib.magic_version_print_version_id
magic_version_print_version_name = lib.magic_version_print_version_name

def pymagic_version_print_full ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"\nPyMagic Version: %s".encode ('utf-8'), PYMAGIC_VERSION_NAME
	)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"Release Date & time: %s - %s".encode ('utf-8'),
		PYMAGIC_VERSION_DATE, PYMAGIC_VERSION_TIME
	)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"Author: %s\n".encode ('utf-8'),
		PYMAGIC_VERSION_AUTHOR
	)

def pymagic_version_print_version_id ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"\nPyMagic Version ID: %s\n".encode ('utf-8'),
		PYMAGIC_VERSION
	)

def pymagic_version_print_version_name ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"\nPyMagic Version: %s\n".encode ('utf-8'),
		PYMAGIC_VERSION_NAME
	)
