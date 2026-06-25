import Data.Array.ST
import Data.Array.Unboxed
import Control.Monad
import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

sieve :: Int -> (Int, Int)
sieve n = runST $ do
    arr <- newArray (0, n) False :: ST s (STUArray s Int Bool)
    writeArray arr 0 True
    when (n > 0) $ writeArray arr 1 True

    forM_ [2..floor (sqrt (fromIntegral n :: Double))] $ \i -> do
        ci <- readArray arr i
        unless ci $
            forM_ [i*i, i*i+i..n] $ \j ->
                writeArray arr j True

    let go k cnt lst
          | k > n     = return (cnt, lst)
          | otherwise = do
              ck <- readArray arr k
              if ck then go (k+1) cnt lst
                    else go (k+1) (cnt+1) k
    go 2 0 (-1)

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let n = read (head (words contents)) :: Int

    start        <- getCurrentTime
    (cnt, last_) <- evaluate (sieve n)
    end          <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
    print cnt
    print last_
    hPutStrLn stderr $ show ms