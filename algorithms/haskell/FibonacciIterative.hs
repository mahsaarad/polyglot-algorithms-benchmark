import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

modVal :: Integer
modVal = 1000000007

fibIter :: Int -> Integer
fibIter 0 = 0
fibIter n = go n 0 1
  where
    go 1 _ b = b `mod` modVal
    go k a b = go (k-1) b ((a+b) `mod` modVal)

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let n = read (head (words contents)) :: Int

    start  <- getCurrentTime
    result <- evaluate (fibIter n)
    end    <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
    print result
    hPutStrLn stderr $ show ms