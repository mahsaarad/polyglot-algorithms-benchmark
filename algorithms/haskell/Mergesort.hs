import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

mergeL :: [Int] -> [Int] -> [Int]
mergeL [] ys = ys
mergeL xs [] = xs
mergeL (x:xs) (y:ys)
    | x <= y    = x : mergeL xs (y:ys)
    | otherwise = y : mergeL (x:xs) ys

mergesort :: [Int] -> [Int]
mergesort []  = []
mergesort [x] = [x]
mergesort xs  =
    let mid         = length xs `div` 2
        (left,right) = splitAt mid xs
    in mergeL (mergesort left) (mergesort right)

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let ws    = words contents
        arr   = map read (tail ws) :: [Int]

    start  <- getCurrentTime
    result <- evaluate (mergesort arr)
    end    <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
    putStrLn $ unwords (map show result)
    hPutStrLn stderr $ show ms