import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

quicksort :: [Int] -> [Int]
quicksort []     = []
quicksort (x:xs) =
    let smaller = quicksort [y | y <- xs, y <= x]
        greater = quicksort [y | y <- xs, y >  x]
    in  smaller ++ [x] ++ greater

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let ws  = words contents
        arr = map read (tail ws) :: [Int]

    start  <- getCurrentTime
    result <- evaluate (quicksort arr)
    end    <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
    putStrLn $ unwords (map show result)
    hPutStrLn stderr $ show ms