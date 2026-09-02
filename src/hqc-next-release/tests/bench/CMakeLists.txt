cmake_minimum_required(VERSION 3.21)
include(CTest)

file(GLOB BENCH_SRCS CONFIGURE_DEPENDS
        "${CMAKE_CURRENT_SOURCE_DIR}/benchmark_*.c"
)

foreach(variant IN LISTS VARIANTS)
    string(REPLACE "-" "_" safe_var ${variant})

    foreach(src IN LISTS BENCH_SRCS)
        get_filename_component(name ${src} NAME_WE)
        set(exe "${name}_${safe_var}")

        add_executable(${exe} ${src})
        target_link_libraries(${exe} PRIVATE
                ${safe_var}_${HQC_ARCH}
                fips202
        )
        target_compile_definitions(${exe} PRIVATE
                $<$<STREQUAL:${HQC_ARCH},x86_64>:AVX2_MODE>
                $<$<NOT:$<STREQUAL:${HQC_ARCH},x86_64>>:REF_MODE>
        )
        target_include_directories(${exe} PRIVATE
                ${CMAKE_SOURCE_DIR}/tests/bench
                ${CMAKE_SOURCE_DIR}/src/common
                ${CMAKE_SOURCE_DIR}/src/${HQC_ARCH}/${variant}
                ${CMAKE_SOURCE_DIR}/lib/fips202
        )

    endforeach()
endforeach()

# NOTE: the unified cross-KEM benchmark does not live here. FrodoKEM, HQC and
# Kaiburr are all benchmarked through the shared driver in src/benchmarks/,
# which links the static libraries this project builds. See
# BENCHMARK_SETUP.md at the repository root.
