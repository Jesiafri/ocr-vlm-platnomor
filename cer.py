import editdistance

def calculate_cer(ground_truth, prediction):
    S = editdistance.eval(ground_truth, prediction)
    N = len(ground_truth)
    if N == 0:
        return 1.0 if prediction else 0.0
    return S / N
