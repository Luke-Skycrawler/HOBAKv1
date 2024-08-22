# CMakeLists.txt
cmake_minimum_required(VERSION 3.19)

# Find dependencies provided by vcpkg (via vcpkg.cmake)
find_package(GLUT REQUIRED)
find_package(glad CONFIG REQUIRED)

set(PROJECT_NAME main)

################################################################################
# Source groups
################################################################################


set(Includes
    "./"
    "ext/eigen-3.3.7" 
    "src/"
    "src/util" 
    "ext/spectra-0.8.1/include" 
    "ext/rapidjson" 
    "ext/glvu/" 
    "ext/rapidjson/" 
)

set(Sources
    "projects/simulateScene/simulateScene.cpp" 
    "ext/glvu/glvu.cpp"
    "src/util/MATRIX_UTIL.cpp"
    "src/util/COLLISION_UTIL.cpp"
    "src/util/FILE_IO.cpp"
    "src/util/TIMER.cpp"
    "src/util/DRAW_GL.cpp"
    "src/Timestepper/BACKWARD_EULER_VELOCITY.cpp"
    "src/Timestepper/BACKWARD_EULER_POSITION.cpp"
    "src/Timestepper/TIMESTEPPER.cpp"
    "src/Timestepper/BDF_1.cpp"
    "src/Timestepper/BDF_2.cpp"
    "src/Timestepper/NEWMARK.cpp"
    "src/Timestepper/QUASISTATIC.cpp"
    "src/Geometry/LINE_INTERSECT.cpp"
    "src/Geometry/CAPSULE.cpp"
    "src/Geometry/CYLINDER.cpp"
    "src/Geometry/CUBE.cpp"
    "src/Geometry/SPHERE.cpp"
    "src/Geometry/AABB_TREE.cpp"
    "src/Geometry/TET_MESH.cpp"
    "src/Geometry/TET_MESH_FASTER.cpp"
    "src/Damping/Volume/GREEN_DAMPING.cpp"
    "src/Hyperelastic/Volume/EDGE_COLLISION.cpp"
    "src/Hyperelastic/Volume/EDGE_SQRT_COLLISION.cpp"
    "src/Hyperelastic/Volume/EDGE_HYBRID_COLLISION.cpp"
    "src/Hyperelastic/Volume/MCADAMS_COLLISION.cpp"
    "src/Hyperelastic/Volume/VERTEX_FACE_COLLISION.cpp"
    "src/Hyperelastic/Volume/VERTEX_FACE_SQRT_COLLISION.cpp"
    "src/Hyperelastic/Volume/ANISOTROPIC_ARAP.cpp"
    "src/Hyperelastic/Volume/ANISOTROPIC_STVK.cpp"
    "src/Hyperelastic/Volume/ANISOTROPIC_FUNG.cpp"
    "src/Hyperelastic/Volume/ANISOTROPIC_DIRICHLET.cpp"
    "src/Hyperelastic/Volume/STVK.cpp"
    "src/Hyperelastic/Volume/SNH.cpp"
    "src/Hyperelastic/Volume/LINEAR.cpp"
    "src/Hyperelastic/Volume/ARAP.cpp"
    "src/Hyperelastic/Volume/HYPERELASTIC.cpp"
)
source_group("Sources" FILES ${Sources})

set(ALL_FILES
    ${Sources}
)

################################################################################
# Target
################################################################################
add_executable(${PROJECT_NAME} ${ALL_FILES})

# # main target
# add_executable(main)
target_include_directories(main PRIVATE 
    ${Includes}
    ${GLM_INCLUDE_DIRS} 
    ${GLFW3_INCLUDE_DIRS} 
    ${ASSIMP_INCLUDE_DIRS} 
    ${GLAD_INCLUDE_DIRS}
)

target_sources(main PRIVATE ${ALL_FILES})
target_link_libraries(main PRIVATE glad::glad GLUT::GLUT)
