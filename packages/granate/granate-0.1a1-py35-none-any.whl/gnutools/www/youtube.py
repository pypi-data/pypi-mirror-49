import os
from gnutools.utils import listfiles, parent, replace_dir
import datetime
import numpy as np

class Youtube:
    def __init__(self, id, sub_lang="ja", root_tmp_dir="/tmp"):
        self.id = id
        self.root_tmp_dir=root_tmp_dir
        self.opts={}
        self.url = "https://www.youtube.com/watch?v={id}".format(id=id)
        self.opts["--sub-lang"] = sub_lang
        self.opts["--extract-audio"] = ""
        self.opts["--audio-format"] = "wav"
        self.opts["--audio-quality"] = "0"
        self.opts["--abort-on-error"] = ""
        self.opts["--write-sub"] = ""

    def download(self, root="./"):
        self.root_output_dir=root
        self.output_dir = "{root}/{id}".format(root=root, id=self.id)
        self.tmp_dir= "{root_tmp_dir}/{id}".format(root_tmp_dir=self.root_tmp_dir, id=self.id)
        [replace_dir(dir) for dir in [self.output_dir, self.tmp_dir]]
        # Download and the audio file with the captions
        commands = ["cd {tmp_dir}; youtube-dl {url} {opts}".format(tmp_dir=self.tmp_dir,
                                                                   url=self.url,
                                                                   opts=" ".join(["{k} {v}".format(k=k, v=v)
                                                                                  for k, v in self.opts.items()])),
                    "mv {tmp_dir} {output_dir}".format(tmp_dir=self.tmp_dir,
                                                       output_dir=parent(self.output_dir))]

        [os.system(command) for command in commands]



    def _reformat_captions(self):
        # Reformat the captions
        vtt_file = listfiles(root=self.output_dir, patterns=[".vtt"])[0]
        captions = {}
        lines = [line.split("\n")[0] for line in open(vtt_file, "r").readlines()]
        stops = [k for k, line in enumerate(lines) if line==""]
        for k, stop in enumerate(stops[:-1]):
            t0, t1 = lines[stop+1].split(" --> ")
            delta = int((datetime.datetime.strptime(t1, '%H:%M:%S.%f') -
                         datetime.datetime.strptime(t0, '%H:%M:%S.%f')).total_seconds())
            caption =" ".join(lines[stop+2:stops[k+1]]).replace("\n", " ")
            captions[k] = {"t0": t0, "t1": t1, "delta": delta, "caption": caption}
        self.captions = captions
        # Write the result
        self.csv_file = vtt_file.replace(".{sub_lang}.vtt".format(sub_lang=self.opts["--sub-lang"]), ".csv")
        self._write_csv()
        # Remove the vtt file
        os.system("rm '{vtt}'".format(vtt=vtt_file))

    def _write_csv(self, filtered=False):
        with open(self.csv_file, "w") as f:
            for k, v in self.captions.items():
                f.write("{t0},{t1},{delta},{caption}\n".format(t0=v["t0"],
                                                               t1=v["t1"],
                                                               delta=v["delta"],
                                                               caption=v["caption"] if not filtered else
                                                               "{caption},{filtered}".format(caption=v["caption"],
                                                                                             filtered=v["filtered"])))

    def _convert_fq(self, fq):
        if fq is not None:
            # Convert the frequency
            from iyo.audio import convert_fq
            self.wav_file = self.csv_file.replace(".csv", ".wav")
            convert_fq(in_file=self.wav_file, out_file=self.wav_file.replace(".wav", ".{fq}.wav".format(fq=fq)), fq=fq)
            os.system("mv '{in_file}' '{out_file}'".format(in_file=self.wav_file.replace(".wav", ".{fq}.wav".format(fq=fq)),
                                                           out_file=self.wav_file))
            # Split the text

    def _split_audio(self, split_audio):
        os.makedirs("{output_dir}/audio".format(output_dir=self.output_dir))
        def convert_time(t):
            t, microseconds = t.split(".")
            t = np.array(t.split(":"), dtype=int)
            t = t[2] + t[1]*60 + t[0]*3600
            t = float("{t}.{microseconds}".format(t=t, microseconds=microseconds))
            return t
        from iyo.audio import slice_audio, read
        sound = read(self.wav_file, backend="pydub")
        for k, v in self.captions.items():
            slice = slice_audio(sound, convert_time(v["t0"]), convert_time(v["t1"]))
            output_file = self.get_name(v, "audio")
            slice.export(output_file, format="wav")

    def get_name(self, v, type):
        output_file = "{output_dir}/{type}/{id}_{t0}_{t1}.{delta}.{ext}".format(output_dir=self.output_dir,
                                                                                id=self.id,
                                                                                t0=v["t0"],
                                                                                t1=v["t1"],
                                                                                type=type,
                                                                                delta=v["delta"],
                                                                                ext="txt" if type=="text" else "wav")
        return output_file

    def _split_captions(self, split_caption):
        from iyo.utils import third_party
        from iyo.nlp import filter
        os.makedirs("{output_dir}/text".format(output_dir=self.output_dir))
        for k, v in self.captions.items():
            output_file = self.get_name(v, "text")
            if self.opts["--sub-lang"]=="ja":
                content = filter(labels=third_party("jp_labels"),
                                 specials=third_party("specials"),
                                 table=third_party("table_jp_labels"),
                                 content=v["caption"])[0]
                self.captions[k]["filtered"]=content
                with open(output_file, "w") as f:
                    f.write("{content}".format(content=content))
        self._write_csv(filtered=True)

    def post_process(self, fq=None, split_audio=True,split_captions=True):
        self._reformat_captions()
        self._convert_fq(fq)
        self._split_audio(split_audio)
        self._split_captions(split_captions)

