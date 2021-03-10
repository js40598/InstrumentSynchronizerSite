# from [[int, int], [int, int], [int, int]] to 'int,int;int,int;int,int'
def encode_samples(samples):
    output = ''
    for sample in samples:
        output += '{},{};'.format(sample[0], sample[1])
    return output[:-1:]


# from 'int,int;int,int;int,int' to [[int, int], [int, int], [int, int]]
def decode_samples(samples):
    output = [sample.split(',') for sample in samples.split(';')]
    return [[int(sample[0]), int(sample[1])] for sample in output]
