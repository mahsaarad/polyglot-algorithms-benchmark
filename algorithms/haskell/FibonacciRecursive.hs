import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

modVal :: Integer
modVal = 1000000007

fib :: Int -> Integer
fib 0 = 0
fib 1 = 1
fib n = (fib (n-1) + fib (n-2)) `mod` modVal

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let n = read (head (words contents)) :: Int

    start  <- getCurrentTime
    result <- evaluate (fib n)
    end    <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
    print result
    hPutStrLn stderr $ show ms