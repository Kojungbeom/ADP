import unittest
import convert.adp_cvt as adp_cvt

class cvtTest(unittest.TestCase):
    function_name = ''
    result = ''
    def test_wav2raw(self):
        self.function_name = 'test_raw2wav'
        boolval = adp_cvt.cvt_wav2raw(
            file_path='samples/test_wav.wav',
            save_path='samples/')
        self.assertTrue(boolval)
        self.result = True

    def test_raw2wav(self):
        self.function_name = 'test_raw2wav'
        boolval = adp_cvt.cvt_raw2wav(
            channels=8,
            sr=16000,
            file_path='samples/test_raw.raw',
            save_path='samples/')
        self.assertTrue(boolval)
        self.result = True

    def tearDown(self):
        if self.result == True:
            print(self.function_name, '...[Success]')
        else:
            print(self.function_name, '...[Fail]')
if __name__ == "__main__":
    unittest.main()
