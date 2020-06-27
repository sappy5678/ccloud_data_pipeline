import luigi
from luigi.contrib.simulate import RunAnywayTarget

<<<<<<< HEAD
import os, json, copy


SENTENCE_JSON_ELEMENT = {
    "sentence": {"origin": None, "Tok": {}, "Pos": {}, "Tag": {}, "Ner": {}, "Dep": {}}
}


class Tokenizer_Task(luigi.Task):
    output_json_path = luigi.Parameter()
    pipline_config = luigi.Parameter()

    def Tok_handler(self, sentence, parser):
        if parser == "spacy":
            try:
                import spacy, en_core_web_sm
            except ImportError:
                print("Can't import spacy")
            nlp = en_core_web_sm.load()
            doc = nlp(sentence)
            return [str(token) for token in doc]
        elif parser == "nltk":
            try:
                import nltk
                from nltk.tokenize.stanford import StanfordTokenizer

                os.environ["CLASSPATH"] = "./StanfordNLP/jars"
                os.environ["STANFORD_MODELS"] = "./StanfordNLP/models"
            except ImportError:
                print("Can't import spacy")
            tokenizer = StanfordTokenizer()
            return tokenizer.tokenize(sentence)

    def check_json(self,):
        pass

    def run(self,):
        with open(self.output_json_path, "r") as f:
            in_out_json = json.load(f)
        config = json.loads(self.pipline_config)
        if int(config["Tok"]) == 1:
            for j in in_out_json["content"]:
                sentence = j["sentence"]["origin"]
                j["sentence"]["Tok"] = self.Tok_handler(sentence, config["parser"])
            with open(self.output_json_path, "w") as f:
                json.dump(in_out_json, f)
        self.output().done()

    def output(self,):
        return RunAnywayTarget(self)


class Dep_Task(luigi.Task):
    output_json_path = luigi.Parameter()
    pipline_config = luigi.Parameter()

    def Dep_handler(self, sentence, parser):
        if parser == "spacy":
            try:
                import spacy, en_core_web_sm
            except ImportError:
                print("Can't import spacy")
            nlp = en_core_web_sm.load()
            doc = nlp(sentence)
            return_dict = {}
            for token in doc:
                return_dict[str(token.text)] = str(token.dep_)
            return return_dict
        elif parser == "nltk":
            try:
                import nltk
                from nltk.parse.stanford import StanfordDependencyParser

                os.environ["CLASSPATH"] = "./StanfordNLP/jars"
                os.environ["STANFORD_MODELS"] = "./StanfordNLP/models"
            except ImportError:
                print("Can't import nltk")
            eng_parser = StanfordDependencyParser()
            res = list(eng_parser.parse(sentence.split()))
            return_dict = {}
            turn = True
            for row in res[0].triples():
                if row[0][0] not in return_dict and turn:
                    return_dict[row[0][0]] = "ROOT"
                    turn = False
                return_dict[row[2][0]] = row[1]
            #     print(row)
            #             print(return_dict)
            return return_dict

    def check_json(self,):
        pass

    def run(self,):
        with open(self.output_json_path, "r") as f:
            in_out_json = json.load(f)
        config = json.loads(self.pipline_config)
        if int(config["Dep"]) == 1:
            for j in in_out_json["content"]:
                sentence = j["sentence"]["origin"]
                j["sentence"]["Dep"] = self.Dep_handler(sentence, config["parser"])
            with open(self.output_json_path, "w") as f:
                json.dump(in_out_json, f)
        self.output().done()

    def output(self,):
        return RunAnywayTarget(self)


class Ner_Task(luigi.Task):
    output_json_path = luigi.Parameter()
    pipline_config = luigi.Parameter()

    def Ner_handler(self, sentence, parser):
        if parser == "spacy":
            try:
                import spacy, en_core_web_sm
            except ImportError:
                print("Can't import spacy")
            nlp = en_core_web_sm.load()
            doc = nlp(sentence)
            return_dict = {}
            for ent in doc.ents:
                return_dict[str(ent.text)] = str(ent.label_)
            return return_dict

        elif parser == "nltk":
            try:
                import nltk
                from nltk.tag import StanfordNERTagger

                os.environ["CLASSPATH"] = "./StanfordNLP/jars"
                os.environ["STANFORD_MODELS"] = "./StanfordNLP/models"
            except ImportError:
                print("Can't import spacy")
            eng_tagger = StanfordNERTagger("english.all.3class.distsim.crf.ser.gz")
            return_dict = {}
            for ner in eng_tagger.tag(sentence.split()):
                if ner[1] != "O":
                    return_dict[str(ner[0])] = str(ner[1])
            #             print(return_dict)
            return return_dict

    def check_json(self,):
        pass

    def run(self,):
        with open(self.output_json_path, "r") as f:
            in_out_json = json.load(f)
        config = json.loads(self.pipline_config)
        if int(config["Ner"]) == 1:
            for j in in_out_json["content"]:
                sentence = j["sentence"]["origin"]
                j["sentence"]["Ner"] = self.Ner_handler(sentence, config["parser"])
            with open(self.output_json_path, "w") as f:
                json.dump(in_out_json, f)
        self.output().done()

    def output(self,):
        return RunAnywayTarget(self)


class Tag_Task(luigi.Task):
    output_json_path = luigi.Parameter()
    pipline_config = luigi.Parameter()

    def Tag_handler(self, sentence, parser):
        if parser == "spacy":
            try:
                import spacy, en_core_web_sm
            except ImportError:
                print("Can't import spacy")
            nlp = en_core_web_sm.load()
            doc = nlp(sentence)
            return_dict = {}
            for token in doc:
                return_dict[str(token.text)] = str(token.tag_)
            return return_dict

        elif parser == "nltk":
            try:
                import nltk
                from nltk import pos_tag, word_tokenize
#                 nltk.download('punkt')
            except ImportError:
                print("Can't import spacy")
            tag = pos_tag(word_tokenize(sentence), tagset="universal")
            return_dict = {}
            for t in tag:
                return_dict[t[0]] = t[1]
            #             print(return_dict)
            return return_dict

    def check_json(self,):
        pass

    def run(self,):
        with open(self.output_json_path, "r") as f:
            in_out_json = json.load(f)
        config = json.loads(self.pipline_config)
        if int(config["Tag"]) == 1:
            for j in in_out_json["content"]:
                sentence = j["sentence"]["origin"]
                j["sentence"]["Tag"] = self.Tag_handler(sentence, config["parser"])
            with open(self.output_json_path, "w") as f:
                json.dump(in_out_json, f)
        self.output().done()

    def output(self,):
        return RunAnywayTarget(self)


class Pos_Task(luigi.Task):
    output_json_path = luigi.Parameter()
    pipline_config = luigi.Parameter()

    def Pos_handler(self, sentence, parser):
        if parser == "spacy":
            try:
                import spacy, en_core_web_sm
            except ImportError:
                print("Can't import spacy")
            nlp = en_core_web_sm.load()
            doc = nlp(sentence)
            return_dict = {}
            for token in doc:
                return_dict[str(token.text)] = str(token.pos_)
            return return_dict

        elif parser == "nltk":
            try:
                import nltk
                from nltk import pos_tag, word_tokenize
#                 nltk.download('punkt')
            except ImportError:
                print("Can't import spacy")
            pos = pos_tag(word_tokenize(sentence))
            return_dict = {}
            for p in pos:
                return_dict[p[0]] = p[1]
            #             print(return_dict)
            return return_dict

    def check_json(self,):
        pass

    def run(self,):
        with open(self.output_json_path, "r") as f:
            in_out_json = json.load(f)
        config = json.loads(self.pipline_config)
        if int(config["Pos"]) == 1:
            for j in in_out_json["content"]:
                sentence = j["sentence"]["origin"]
                j["sentence"]["Pos"] = self.Pos_handler(sentence, config["parser"])
            with open(self.output_json_path, "w") as f:
                json.dump(in_out_json, f)
        self.output().done()

    def output(self,):
        return RunAnywayTarget(self)


class Entry(luigi.Task):
    input_path = luigi.Parameter(default="this is json")
    base_path = "./data/"

    def requires(self,):
        return [
            Tokenizer_Task(
                output_json_path=self.output_json_path,
                pipline_config=self.pipline_config,
            ),
            Pos_Task(
                output_json_path=self.output_json_path,
                pipline_config=self.pipline_config,
            ),
            Tag_Task(
                output_json_path=self.output_json_path,
                pipline_config=self.pipline_config,
            ),
            Ner_Task(
                output_json_path=self.output_json_path,
                pipline_config=self.pipline_config,
            ),
            Dep_Task(
                output_json_path=self.output_json_path,
                pipline_config=self.pipline_config,
            ),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sample_out_path = "./data/sample_output.json"

        self.input_json_path = os.path.join(
            os.path.join(self.base_path, "input"), self.input_path
        )
        self.output_json_path = os.path.join(
            os.path.join(self.base_path, "output"), self.input_path
        )
        print("start writing json")
        with open(self.sample_out_path, "r") as f:
            sample_out_json = json.load(f)
        with open(self.input_json_path, "r") as f:
            input_json = json.load(f)
        #         if input_json['pipline']['parser'] == 'spacy':
        #             try:
        #                 import spacy, en_core_web_sm
        #             except ImportError:
        #                 print('Can\'t import spacy')
        #         elif input_json['pipline']['parser'] == 'nltk':
        #             try:
        #         import spacy, en_core_web_sm
        self.pipline_config = json.dumps(input_json["pipline"])
        print("pipline config", type(self.pipline_config))

        sample_out_json["id"] = input_json["id"]
        sample_out_json["title"] = input_json["title"]
        sample_out_json["metadata"] = input_json["metadata"]

        for idx, con in enumerate(input_json["content"]):
            sample_out_json["content"].append(copy.deepcopy(SENTENCE_JSON_ELEMENT))
            sample_out_json["content"][-1]["sentence"]["origin"] = con["sentence"][
                "origin"
            ]
        print(self.pipline_config)
        print(sample_out_json)

        # set sample output file
        #         sample['content'][0]['sentence']['origin'] = self.input_paragraph
        with open(self.output_json_path, "w") as f:
            json.dump(sample_out_json, f)

    #         print(json.dumps(sample, indent=2))

    def run(self,):
        print("Finish")


if __name__ == "__main__":
    luigi.run()
=======
import os, json

import spacy, en_core_web_sm

class Tokenizer_Task(luigi.Task):
    out_path = luigi.Parameter()
    threshold = luigi.Parameter()
    
    def Tokenizer_handler(self, paragraph):
        nlp = en_core_web_sm.load()
        doc = nlp(paragraph)
        return [str(token) for token in doc ]
    
    def check_json(self, ):
        pass
    
    def run(self, ):
        with open(self.out_path, 'r') as f:
            in_out_json = json.load(f)
        if int(self.threshold) == 1:
            paragraph = in_out_json['content'][0]['sentence']['origin']
            in_out_json['content'][0]['sentence']['Tok'] = self.Tokenizer_handler(paragraph)
            with open(self.out_path, 'w') as f:
                json.dump(in_out_json, f)
        self.output().done()

    def output(self, ):
        return RunAnywayTarget(self)
    
class Dep_Task(luigi.Task):
    out_path = luigi.Parameter()
    threshold = luigi.Parameter()

    def Dep_handler(self, paragraph):
        nlp = en_core_web_sm.load()
        doc = nlp(paragraph)
        return_dict = {}
        for token in doc:
            return_dict[str(token.text)] = str(token.dep_)
        return return_dict
    
    def check_json(self, ):
        pass
    
    def run(self, ):
        with open(self.out_path, 'r') as f:
            in_out_json = json.load(f)
        if int(self.threshold) == 1:
            paragraph = in_out_json['content'][0]['sentence']['origin']
            in_out_json['content'][0]['sentence']['Dep'] = self.Dep_handler(paragraph)
            with open(self.out_path, 'w') as f:
                json.dump(in_out_json, f)
        self.output().done()

    def output(self, ):
        return RunAnywayTarget(self)
    
class Ner_Task(luigi.Task):
    out_path = luigi.Parameter()
    threshold = luigi.Parameter()

    def Ner_handler(self, paragraph):
        nlp = en_core_web_sm.load()
        doc = nlp(paragraph)
        return_dict = {}
        for ent in doc.ents:
            return_dict[str(ent.text)] = str(ent.label_)
        return return_dict
    
    def check_json(self, ):
        pass
    
    def run(self, ):
        with open(self.out_path, 'r') as f:
            in_out_json = json.load(f)
        if int(self.threshold) == 1:
            paragraph = in_out_json['content'][0]['sentence']['origin']
            in_out_json['content'][0]['sentence']['Ner'] = self.Ner_handler(paragraph)
            with open(self.out_path, 'w') as f:
                json.dump(in_out_json, f)
        self.output().done()

    def output(self, ):
        return RunAnywayTarget(self)
    
    
    
class Tag_Task(luigi.Task):
    out_path = luigi.Parameter()
    threshold = luigi.Parameter()

    def Tag_handler(self, paragraph):
        import en_core_web_sm
        nlp = en_core_web_sm.load()
        doc = nlp(paragraph)
        return_dict = {}
        for token in doc:
            return_dict[str(token.text)] = str(token.tag_)
        return return_dict
    
    def check_json(self, ):
        pass
    
    def run(self, ):
        with open(self.out_path, 'r') as f:
            in_out_json = json.load(f)
        if int(self.threshold) == 1:
            paragraph = in_out_json['content'][0]['sentence']['origin']
            in_out_json['content'][0]['sentence']['Tag'] = self.Tag_handler(paragraph)
            with open(self.out_path, 'w') as f:
                json.dump(in_out_json, f)
        self.output().done()

    def output(self, ):
        return RunAnywayTarget(self)
    
    
    
class Pos_Task(luigi.Task):
    out_path = luigi.Parameter()
    threshold = luigi.Parameter()

    def Pos_handler(self, paragraph):
        nlp = en_core_web_sm.load()
        doc = nlp(paragraph)
        return_dict = {}
        for token in doc:
            return_dict[str(token.text)] = str(token.pos_)
        return return_dict
    
    def check_json(self, ):
        pass
    
    def run(self, ):
        with open(self.out_path, 'r') as f:
            in_out_json = json.load(f)
            
        if int(self.threshold) == 1:
            paragraph = in_out_json['content'][0]['sentence']['origin']
            in_out_json['content'][0]['sentence']['Pos'] = self.Pos_handler(paragraph)
            with open(self.out_path, 'w') as f:
                json.dump(in_out_json, f)
        self.output().done()

    def output(self, ):
        return RunAnywayTarget(self)
    
    
    
class Entry(luigi.Task):
    input_path = luigi.Parameter(default='this is json')
    input_paragraph = luigi.Parameter()
    input_pipline = luigi.Parameter()
    base_path = './data/'

    def requires(self, ):
        return [Tokenizer_Task(out_path= self.output_path, threshold = self.pipline_dict['Tok']), 
                Pos_Task(out_path = self.output_path, threshold = self.pipline_dict['Pos']), 
                Tag_Task(out_path = self.output_path, threshold = self.pipline_dict['Tag']), 
                Ner_Task(out_path = self.output_path, threshold = self.pipline_dict['Ner']),
                Dep_Task(out_path = self.output_path, threshold = self.pipline_dict['Dep'])]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sample_path = './data/sample_output.json'

        self.output_path = os.path.join(
                            os.path.join(self.base_path, 'output'),
                            self.input_path
                        )
        print('start writing json')
        self.pipline_dict = json.loads(self.input_pipline)
        with open(self.sample_path, 'r') as f:
            sample = json.load(f)

        sample['content'][0]['sentence']['origin'] = self.input_paragraph
        with open(self.output_path, 'w') as f:
            json.dump(sample, f)
        with open(self.output_path, 'r') as f:
            sample = json.load(f)
#         print(json.dumps(sample, indent=2))
        
    def run(self, ):
        print('Finish')

        
if __name__ == '__main__':
    luigi.run()
>>>>>>> d113409810a9634d308c8867bcb3c9861c4d389d
