
import Levenshtein as Lev

def calculate_cer(s1, s2):
    """
    Computes the Character Error Rate, defined as the edit distance.

    Arguments:
        s1 (string): space-separated sentence (actual)
        s2 (string): space-separated sentence (predicted)
    """
    s1 = s1.replace(' ', '')
    s2 = s2.replace(' ', '')
    return Lev.distance(s1, s2)/len(s1)

def calculate_wer(s1, s2):
    """
    Computes the Word Error Rate, defined as the edit distance between the
    two provided sentences after tokenizing to words.
    Arguments:
        s1 (string): space-separated sentence
        s2 (string): space-separated sentence
    """

    # build mapping of words to integers
    b = set(s1.split() + s2.split())
    word2char = dict(zip(b, range(len(b))))

    # map the words to a char array (Levenshtein packages only accepts
    # strings)
    w1 = [chr(word2char[w]) for w in s1.split()]
    w2 = [chr(word2char[w]) for w in s2.split()]

    return Lev.distance(''.join(w1), ''.join(w2)) / len(s1.split())
    


def calculate_cer_list_pair(results):
    """
    Arguments:
        results (list): list of ground truth and
            predicted sequence pairs.

    Returns the CER for the full set.
    """
    dist = sum(Lev.distance(label, pred)
                for label, pred in results)
    total = sum(len(label) for label, _ in results)
    return dist / total

    
def compute_wer_list_pair(results):

    dist = []
    total_len = []
    for label, pred in results:
        #print("".join(label))
        dist.append(wer("".join(label), "".join(pred)))
        total_len.append(len("".join(label).split()))
     
    return sum(dist)/sum(total_len)

def wer(s1,s2):
    """
    Computes the Word Error Rate, defined as the edit distance between the
    two provided sentences after tokenizing to words.
    Arguments:
        s1 (string): space-separated sentence
        s2 (string): space-separated sentence
    """
    # build mapping of words to integers
    b = set(s1.split() + s2.split())
    word2char = dict(zip(b, range(len(b))))

    # map the words to a char array (Levenshtein packages only accepts
    # strings)
    w1 = [chr(word2char[w]) for w in s1.split()]
    w2 = [chr(word2char[w]) for w in s2.split()]

    return Lev.distance(''.join(w1), ''.join(w2))
    