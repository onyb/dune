import subprocess
import sys

def _convert_subprocess_cmd(cmd):
	if OS == 'Windows':
		if '"' in cmd:
			# Assume there's only one quoted argument.
			bits = cmd.split('"')
			return bits[0].split() + [bits[1]] + bits[2].split()
		else:
			return cmd.split()
		else:
			return [cmd]

def _perror(e):
	print("subprocess.CalledProcessError: Command '%s' returned non-zero exit status %s" % (
		' '.join(e.cmd), str(e.returncode)))
	#cleanup()
	# Communicate return code to the calling program if any
	sys.exit(e.returncode)

def exec_subprocess_call(cmd, cwd):
	cmd = _convert_subprocess_cmd(cmd)
	try:
		subprocess.check_call(cmd, cwd=cwd, shell=True,
					stdin=subprocess.PIPE, stdout=None, stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError as e:
		_perror(e)

def exec_subprocess_check_output(cmd, cwd):
	cmd = _convert_subprocess_cmd(cmd)
	try:
		out = subprocess.check_output(cmd, cwd=cwd, shell=True,
					stdin=subprocess.PIPE, stderr=subprocess.STDOUT).decode('utf-8')
	except subprocess.CalledProcessError as e:
			_perror(e)
	finally:
		return out

