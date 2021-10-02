# -*- coding: utf-8 -*-
import httpx
import ujson
from loguru import logger
from package import oppadc


class StdInfo:
    """
    返回gosu关于std成绩的相应信息
    """

    def __init__(self):
        try:
            r = httpx.get('http://localhost:24050/json')
        except Exception as e:
            logger.error(f'无法获取gosu的信息，请检查是否开启 {e}')
            return
        self.info = r.json()
        # self.info = ujson.load(open('gosu.json', encoding='gb18030', errors='ignore'))
        self.map = MapInfo(
            self.info['settings']['folders']['songs'] + '\\' + self.info['menu']['bm']['path']['folder'] +
            '\\' + self.info['menu']['bm']['path']['file'])

    def state(self):
        return self.info['menu']['state']

    def ur(self):
        return self.info['gameplay']['hits']['unstableRate']

    def map_status(self):
        return self.info['menu']['bm']['rankedStatus']

    def mode(self):
        return self.info['menu']['gameMode']

    def map_dir(self):
        return (self.info['settings']['folders']['songs'] + '\\' + self.info['menu']['bm']['path']['folder'] +
                '\\' + self.info['menu']['bm']['path']['file'])

    def songs_dir(self):
        return self.info['settings']['folders']['songs']

    def bg_dir(self):
        return self.info['settings']['folders']['songs'] + '\\' + self.info['menu']['bm']['path']['full']

    def title(self):
        i = self.info['menu']['bm']['metadata']['title']
        return i

    def artist(self):
        return self.info['menu']['bm']['metadata']['artist']

    def cs(self):
        return self.info['menu']['bm']['stats']['CS']

    def ar(self):
        return self.info['menu']['bm']['stats']['AR']

    def od(self):
        return self.info['menu']['bm']['stats']['OD']

    def hp(self):
        return self.info['menu']['bm']['stats']['HP']

    def bpm_min(self):
        return self.info['menu']['bm']['stats']['BPM']['min']

    def bpm_max(self):
        return self.info['menu']['bm']['stats']['BPM']['max']

    def bid(self):
        return self.info['menu']['bm']['id']

    def sid(self):
        return self.info['menu']['bm']['set']

    def c300(self):
        return self.info['gameplay']['hits']['300']

    def c100(self):
        return self.info['gameplay']['hits']['100']

    def c50(self):
        return self.info['gameplay']['hits']['50']

    def c0(self):
        return self.info['gameplay']['hits']['0']

    def stars(self):
        return self.info['menu']['bm']['stats']['fullSR']

    def slider_breaks(self):
        return self.info['gameplay']['hits']['sliderBreaks']

    def pp_current(self):
        return self.info['gameplay']['pp']['current']

    def player_name(self):
        return self.info['gameplay']['name']

    def pp_ss(self):
        return self.info['menu']['pp']['100']

    def pp_99(self):
        return self.info['menu']['pp']['99']

    def pp_98(self):
        return self.info['menu']['pp']['98']

    def pp_97(self):
        return self.info['menu']['pp']['97']

    def pp_96(self):
        return self.info['menu']['pp']['96']

    def pp_95(self):
        return self.info['menu']['pp']['95']

    def pp_fc(self):
        return self.info['gameplay']['pp']['fc']

    def mapper(self):
        return self.info['menu']['bm']['metadata']['mapper']

    def difficulty(self):
        return self.info['menu']['bm']['metadata']['difficulty']

    def key_count_k1(self):
        return self.info['gameplay']['keyOverlay']['k1']['count']

    def key_count_k2(self):
        return self.info['gameplay']['keyOverlay']['k2']['count']

    def key_count_m1(self):
        return self.info['gameplay']['keyOverlay']['m1']['count']

    def key_count_m2(self):
        return self.info['gameplay']['keyOverlay']['m2']['count']

    def score(self):
        return self.info['gameplay']['score']

    def max_combo(self):
        return self.info['gameplay']['combo']['max']

    def accuracy(self):
        return self.info['gameplay']['accuracy']

    def time_length_full(self):
        return self.info['menu']['bm']['time']['full']

    def time_length_now(self):
        return self.info['menu']['bm']['time']['current']

    def mod_str(self):
        return self.info['menu']['mods']['str']

    def rank_result(self):
        return self.info['gameplay']['hits']['grade']['current']

    def pp_strains(self):
        return self.info['menu']['pp']['strains']

    def ur_strains(self):
        return self.info['gameplay']['hits']['hitErrorArray']

    def countCircle(self):
        return self.map.circle()

    def countSlider(self):
        return self.map.slider()

    def countSpinner(self):
        return self.map.spinner()


class MapInfo:
    def __init__(self, mapDir):
        self.map = oppadc.OsuMap(file_path=mapDir)

    def circle(self):
        return self.map.amount_circle

    def slider(self):
        return self.map.amount_slider

    def spinner(self):
        return self.map.amount_spinner
