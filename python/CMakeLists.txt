pybind11_add_module(python-bindings generate-python-bindings.cpp pybind11_Image.hpp pybind11_optional.hpp pybind11_variant.hpp)
target_link_libraries(python-bindings PRIVATE eos)
set_target_properties(python-bindings PROPERTIES OUTPUT_NAME eos)

install(TARGETS python-bindings DESTINATION python)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/demo.py DESTINATION python)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/demo.ipynb DESTINATION python)
