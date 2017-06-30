video_src = "../../data/scraped_data/video/raw/*.mp4"
video_file_path_list = Dir[video_src]

video_file_path_list.each{|file_path|
    file_name = file_path.match('^.*\/(.+?).mp4')[1]
    target_dir = "../../data/scraped_data/video/encoded/#{file_name}/"
    `mkdir -p #{target_dir}`
    # `ffmpeg -i #{file_path} ../../data/scraped_data/video/encoded/#{file_name}.avi`
    `ffmpeg -i #{file_path} -f image2 -vcodec png -r 30 "#{target_dir}%05d.png"`
}