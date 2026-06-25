import Data.Word (Word32)
import Data.Bits (shiftR)
import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

lcgNext :: Word32 -> (Double, Word32)
lcgNext s =
    let s' = s * 1664525 + 1013904223
        x  = fromIntegral (s' `shiftR` 1) / fromIntegral (1 `shiftR` 1 :: Word32)
    in (x, s')

simulate :: Int -> Word32 -> Int
simulate n seed = go n seed 0
  where
    go 0 _ acc = acc
    go k s acc =
        let (x, s' ) = lcgNext s
            (y, s'') = lcgNext s'
            hit      = if x*x + y*y <= 1.0 then 1 else 0
        in go (k-1) s'' (acc + hit)

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let ws   = words contents
        n    = read (head ws) :: Int
        seed = read (ws !! 1) :: Word32

    start  <- getCurrentTime
    inside <- evaluate (simulate n seed)
    end    <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
        pi_ = 4.0 * fromIntegral inside / fromIntegral n :: Double
    putStrLn $ show pi_
    hPutStrLn stderr $ show ms