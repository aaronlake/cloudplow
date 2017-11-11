import logging
import shlex
import subprocess

try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote

log = logging.getLogger('rclone')


class Rclone:
    def __init__(self, name, config, dry_run=False):
        self.name = name
        self.config = config
        self.dry_run = dry_run
        self.extras = self.__extras2string()

    def delete_file(self, path):
        try:
            log.debug("Deleting file '%s' from remote %s", path, self.name)

        except:
            log.exception("Exception deleting file '%s' from remote %s: ", path, self.name)
        return False

    def delete_folder(self, path):
        log.debug("Deleting folder '%s' from remote %s", path, self.name)

    # internals
    def __extras2string(self):
        return ' '.join(
            "%s=%s" % (key, cmd_quote(value) if isinstance(value, str) else value) for (key, value) in
            self.config['rclone_extras'].items()).replace('=None', '').strip()

    @staticmethod
    def __exec(command, callback=None):
        total_output = ''
        process = subprocess.Popen(shlex.split(command), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            output = str(process.stdout.readline()).lstrip('b').replace('\\n', '')
            if process.poll() is not None:
                break
            if output and len(output) > 6:
                log.debug(output)
                if callback:
                    callback(output)
                else:
                    total_output += output

        if not callback:
            return total_output
        rc = process.poll()
        return rc
