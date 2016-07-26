require 'cgi'
require 'json'


page_source = open("../../data/scraped_data/index.html", &:read)

class NoteImageDownloader
    def getImageData(page_source)
		list_data = page_source.scan(%r!<tr class=\"type-(.+?)\">.*?<td>(.+?)</td><td.*?>(.*?)</td><td.*?><a href=\"(.+?)".*?>.*?</a></td><td.*?><a href=\"(.+?)\".*?>.*?</a></td><td.*?"><a href=\"(.+?)\".*?>.*?</a></td><td.*?><a href=\"(.+?)\".*?>.*?</a></td><td.*?></td></tr>!)
		return list_data.reject{|item|
			# Listの整列用ライブラリのせいで楽譜情報でないものが混ざってくるので除去する
			item[1].match(/^<a class/)
		}.map{|item|
			# 属性 (cool, passion, cute, all)
			type = item[0]
			# 楽曲タイトル
			title = CGI.unescapeHTML(item[1])
			bpm = item[2]
			# 難易度名
			level_names = ['debut', 'regular', 'pro', 'master']
			{
				:type => type,
				:title => title,
				:bpm => bpm,
				:resources => item[3,5].zip(level_names).map {|uri, level_name|
					img_pos = uri.sub(/\/view/, 'pattern')
					file_name = "#{type}_#{img_pos.gsub(/\//, '_')}_#{level_name}"
					{
						:note_src_path => "https://deresute.info/#{img_pos}.png?v=1.1.2",
						:file_name => file_name,
						:level => level_name
					}
				}
			}
		}
	end

	def downloadImage(image_data, root_dir)
		image_data.map{|item|
			item[:resources].map{|resouce|
				src = resouce[:note_src_path]
				file_name = "#{root_dir}/#{resouce[:file_name]}.png"
				`wget #{src} -O #{file_name}`
			}
		}
	end

	def saveAsJson(image_data, path)
		File.open(path, "w"){|file|
			json = JSON.pretty_generate(image_data)
			file.puts(json)
		}
	end
end

noteImageDownloader = NoteImageDownloader.new()
image_data = noteImageDownloader.getImageData(page_source)
noteImageDownloader.downloadImage(image_data, '../../data/scraped_data/note_image')
noteImageDownloader.saveAsJson(image_data, '../../data/scraped_data/video_list.json')