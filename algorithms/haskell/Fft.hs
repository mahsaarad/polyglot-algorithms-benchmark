import Data.Complex
import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)
import Data.Bits (shiftR, xor, (.&.))

-- bit-reversal
bitReverse :: [Complex Double] -> [Complex Double]
bitReverse xs = map snd $ sortByIndex $ zip (map rev [0..]) xs
  where
    n    = length xs
    bits = floor (logBase 2 (fromIntegral n) :: Double) :: Int
    rev i = foldl (\acc b -> acc*2 + (i `shiftR` b .&. 1)) 0 [0..bits-1]
    sortByIndex ps = map snd $ foldr insert [] $ zip (map fst ps) ps
      where insert x [] = [x]
            insert x (y:ys)
              | fst x <= fst y = x : y : ys
              | otherwise      = y : insert x ys

fft :: [Complex Double] -> [Complex Double]
fft xs = go (length xs) (bitReverse xs)
  where
    go 1 a  = a
    go n a  =
        let half    = n `div` 2
            evens   = go half (take half a)
            odds    = go half (drop half a)
            twiddle = [ cis (2 * pi * fromIntegral k / fromIntegral n)
                      | k <- [0..half-1] ]
            ts      = zipWith (*) twiddle odds
        in zipWith (+) evens ts ++ zipWith (-) evens ts

-- iterative Cooley-Tukey روی لیست
fftIter :: [Complex Double] -> [Complex Double]
fftIter input = fft input

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let ls   = lines contents
        n    = read (head ls) :: Int
        vals = map read (words (ls !! 1)) :: [Double]
        arr  = map (:+ 0) vals :: [Complex Double]

    start  <- getCurrentTime
    result <- evaluate (fftIter arr)
    end    <- getCurrentTime

    let ms  = realToFrac (diffUTCTime end start) * 1000 :: Double
        k   = min 5 n
        s   = sum $ map magnitude (take k result)
    putStrLn $ show s
    hPutStrLn stderr $ show ms