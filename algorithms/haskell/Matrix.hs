import Data.Array.Unboxed
import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

type Mat = UArray (Int,Int) Int64

readMat :: Int -> [Int64] -> Mat
readMat n xs =
    listArray ((0,0),(n-1,n-1)) xs

multiply :: Int -> Mat -> Mat -> Mat
multiply n a b =
    array ((0,0),(n-1,n-1))
        [ ((i,j), sum [ a!(i,k) * b!(k,j) | k <- [0..n-1] ])
        | i <- [0..n-1], j <- [0..n-1] ]

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let ws    = map read (words contents) :: [Int64]
        n     = fromIntegral (head ws) :: Int
        rest  = tail ws
        aVals = take (n*n) rest
        bVals = take (n*n) (drop (n*n) rest)
        a     = readMat n aVals
        b     = readMat n bVals

    start  <- getCurrentTime
    result <- evaluate (multiply n a b)
    end    <- getCurrentTime

    let ms       = realToFrac (diffUTCTime end start) * 1000 :: Double
        checksum = sum (elems result)
    print checksum
    hPutStrLn stderr $ show ms