from pygments import token
from pygments import lexers
import pygments
import pygments.lexer
from src.models.submission import Submission
import numpy as np
from src.models.file import File


def tokenize(doc):

    try:
        lexer = lexers.get_lexer_by_name(doc.language)
    except:
        lexer = lexers.get_lexer_for_filename(doc.name)

    print(lexer)
    tokens = lexer.get_tokens(text=doc.content)
    
    result = ""
    current_pos = 0
    pos_pairs = [[0, 0]]
    

    for t in tokens:
        if t[0] in token.Name or t in token.Name.Variable or t in token.Name.Attribute:
            result += "V"
            pos_pairs.append([len(result) - 1, current_pos])
            current_pos += len(t[1]) - 1
        elif t[0] in token.Name.Function:
            result += "F"
            pos_pairs.append([len(result) - 1, current_pos])
            current_pos += len(t[1]) - 1
        elif t[0] in token.Name.Class:
            result += "C"
            pos_pairs.append([len(result) - 1, len(t[1]) - 1])
            current_pos += len(t[1]) - 1
        elif t[0] in token.Comment.Preproc or t[0] == token.Comment.Hashbang:
            result += "P"
            pos_pairs.append([len(result) - 1, current_pos])
            current_pos += len(t[1]) - 1
        elif t[0] in token.Text or t[0] in token.Comment:
            pos_pairs.append([len(result) - 1, current_pos])
            current_pos += len(t[1])
        elif t[0] in token.Literal.String:
            if t[1] == "'" or t[1] == '"':
                result += '"'
            else:
                result += "S"
                pos_pairs.append([len(result) - 1, current_pos])
                current_pos += len(t[1]) - 1
        else:
            result += t[1]
        
    
    return result, np.array(pos_pairs)





