require "yaml"
require "uri"
require "faraday"
require 'json'


config = YAML.load_file('config.yaml')
api_key = config['google']['api_key']

class VideoDownloader
    def initialize(api_key)
        uri = "https://www.googleapis.com"
        @api_key = api_key
        @connection = Faraday::Connection.new(:url => uri) do |builder|
            builder.use Faraday::Request::UrlEncoded
            builder.use Faraday::Response::Logger
            builder.use Faraday::Adapter::NetHttp
        end
    end

    def getVideoIds(query)
        q = URI.encode(query)
        response = @connection.get "/youtube/v3/search?part=snippet&key=#{@api_key}&q=#{q}"

        res_obj = JSON.parse(response.body)
        items = res_obj["items"]
        videoIds = []
        titles = []
        items.each{|item|
            if item["kind"] == "youtube#searchResult" && item["id"]["kind"] == "youtube#video" then
                videoId = item["id"]["videoId"]
                videoIds << videoId
                title = item['snippet']['title']
                titles << title
            end
        }
        return videoIds, titles
    end

    def downloadVideo(videoId, filename)
        # 最低画質(動画のみ.mp4)/最低画質(動画&音声.mpr)/最低画質(動画のみ)/最低画質(動画&音声)の優先度でダウンロード
        `youtube-dl -f 'worstvideo[ext=mp4]/worst[ext=mp4]/worstvideo/worst' -o '#{filename}.%(ext)s' #{videoId}`
    end

    def searchAndDownload(query, filename)
        videoIds, titles = getVideoIds(query)
        if videoIds.length != 0 then
            File.open("./download.log", "a"){|file|
                file.puts("#{filename} : #{titles[0]} (#{videoIds[0]})")
            }
            self.downloadVideo(videoIds[0], filename)
        end
    end
end

videoDowanloader = VideoDownloader.new(api_key)

file = File.read('../../data/scraped_data/song_list.json')
song_list = JSON.parse(file)

song_list.each{|song|
    query = "デレステ #{song['title']} #{song['difficulty']}"
    output_file = "../../data/scraped_data/video/raw/#{song['file_name']}"
    videoDowanloader.searchAndDownload(query, output_file)
}