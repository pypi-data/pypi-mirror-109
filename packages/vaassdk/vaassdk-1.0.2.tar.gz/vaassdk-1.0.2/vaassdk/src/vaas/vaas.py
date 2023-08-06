# all vaas api service
import tools
import config


class Vaas():
    def __init__(self, udid):
        self.tool = tools.Tools(udid)
        self.isplay = config.HOST_PROD_PLAY
        self.unplay = config.HOST_PROD

    def feed(self, video_type, channel_id, load_type=0, size=8):
        input = {'video_type': video_type, 'channel_id': channel_id, 'load_type': load_type, 'size': size}
        self.tool.set_input(input)
        ret = self.tool.request_api(self.unplay + config.FEED)
        return ret

    def relation(self, id, size=20):
        input = {'id': id, 'size': size}
        self.tool.set_input(input)
        ret = self.tool.request_api(self.unplay + config.RELATION)
        return ret

    def channels(self):
        ret = self.tool.request_api(self.unplay + config.CHANNELS)
        return ret

    def detail(self, ids, video_type):
        input = {'ids': ids, 'video_type': video_type}
        self.tool.set_input(input)
        ret = self.tool.request_api(self.unplay + config.DETAIL)
        return ret

    def cpinfo(self, id, video_type):
        input = {'id': id, 'video_type': video_type}
        self.tool.set_input(input)
        ret = self.tool.request_api(self.unplay + config.CPINFO)
        return ret

    def cpvideos(self, id, video_type, page=1, size=20):
        input = {'id': id, 'video_type': video_type, 'page': page, 'size': size}
        self.tool.set_input(input)
        ret = self.tool.request_api(self.unplay + config.CPVIDOES)
        return ret

    def play(self, id):
        input = {'id': id}
        self.tool.set_input(input)
        ret = self.tool.request_api(self.isplay + config.PLAY)
        return ret