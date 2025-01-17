from augur.tasks.git.dependency_tasks.dependency_util import python_deps
from augur.tasks.git.dependency_tasks.dependency_util import ruby_deps
from augur.tasks.git.dependency_tasks.dependency_util import php_deps
from augur.tasks.git.dependency_tasks.dependency_util import javascript_deps
from augur.tasks.git.dependency_tasks.dependency_util import vb_deps
from augur.tasks.git.dependency_tasks.dependency_util import csharp_deps
from augur.tasks.git.dependency_tasks.dependency_util import java_deps
from augur.tasks.git.dependency_tasks.dependency_util import cpp_deps
from augur.tasks.git.dependency_tasks.dependency_util import c_deps
from augur.tasks.git.dependency_tasks.dependency_util import dependency_calculator

class Dep:
	def __init__(self, name, language, count):
		self.name = name
		self.language = language
		self.count = count
	def __repr__(self):
		return f'Dep(name={self.name}, language={self.language}, count={self.count})'

def get_deps(path):
	deps = []
	deps.extend(get_language_deps(path, python_deps, 'python'))
	deps.extend(get_language_deps(path, ruby_deps, 'ruby'))
	deps.extend(get_language_deps(path, php_deps, 'php'))
	deps.extend(get_language_deps(path, javascript_deps, 'javascript'))
	deps.extend(get_language_deps(path, vb_deps, 'visual basic'))
	deps.extend(get_language_deps(path, csharp_deps, 'C#'))
	deps.extend(get_language_deps(path, java_deps, 'java'))
	deps.extend(get_language_deps(path, cpp_deps, 'C++'))
	deps.extend(get_language_deps(path, c_deps, 'C'))
	return deps
	
def get_language_deps(path, language, name):
	files = language.get_files(path)
	deps_map = {}
	for f in files:
		f_deps = language.get_deps_for_file(f)
		if f_deps is None:
			continue
		for dep in f_deps:
			if dep in deps_map:
				deps_map[dep].count += 1
			else:
				deps_map[dep] = Dep(dep, name, 1)
	return list(deps_map.values())
