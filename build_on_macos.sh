#!/bin/bash
build_dir=build

boost_root=$(brew --prefix boost)
echo "--> boost_root: ${boost_root}"

python_root_dir=$(python -c "import sys; print(sys.prefix)")
python_include_dirs=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")

echo "--> python_root_dir: ${python_root_dir}"
echo "--> python_include_dirs: ${python_include_dirs}"

if [ ! -d ${build_dir} ]; then
    echo "--> build_dir does not exist, creating it"
else
    echo "--> build_dir exists, removing it"
    rm -rf ${build_dir}
fi

mkdir ${build_dir}
cd ${build_dir}
# cmake ../ -DCMAKE_INSTALL_PREFIX=../install/
# cmake ../ -DCMAKE_INSTALL_PREFIX=../install/ -DBOOST_ROOT=${boost_root} -DEOS_GENERATE_PYTHON_BINDINGS=1
# cmake ../ -DCMAKE_INSTALL_PREFIX=../install/ -DEOS_GENERATE_PYTHON_BINDINGS=1 -DPython_ROOT_DIR=${python_root_dir} -DBOOST_ROOT=${boost_root}
cmake ../ -DCMAKE_INSTALL_PREFIX=../install/ -DEOS_GENERATE_PYTHON_BINDINGS=1 -DPython_ROOT_DIR=${python_root_dir} -DPYTHON_INCLUDE_DIRS=${python_include_dirs} -DBOOST_ROOT=${boost_root}
make -j8
make install
cd ..