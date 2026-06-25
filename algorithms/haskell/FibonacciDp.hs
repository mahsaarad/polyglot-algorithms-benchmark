import Data.Array.Unboxed
import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

modVal :: Integer
modVal = 1000000007

fibDP :: Int -> Integer
fibDP n =
    let dp = listArray (0, n)
               (0 : 1 : [((dp ! (i-1)) + (dp ! (i-2))) `mod` modVal
                         | i <- [2..n]]) :: Array Int Integer
    in dp ! n

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let n = read (head (words contents)) :: Int

    start  <- getCurrentTime
    result <- evaluate (fibDP n)
    end    <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
    print result
    hPutStrLn stderr $ show ms