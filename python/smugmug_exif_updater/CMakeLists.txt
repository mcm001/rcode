project(exif_meme)

add_executable(meme test.cpp)
target_link_libraries(meme exiv2)
