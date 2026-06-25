import Data.Array.Unboxed
import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

lcs :: String -> String -> Int
lcs a b =
    let n   = length a
        m   = length b
        av  = listArray (1,n) a :: UArray Int Char
        bv  = listArray (1,m) b :: UArray Int Char
        dp  = array ((0,0),(n,m)) [((i,j), cell i j) | i<-[0..n], j<-[0..m]]
        cell 0 _ = 0
        cell _ 0 = 0
        cell i j
            | av ! i == bv ! j = dp ! (i-1, j-1) + 1
            | otherwise        = max (dp ! (i-1, j)) (dp ! (i, j-1))
    in dp ! (n, m)

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let ls = lines contents
        a  = head ls
        b  = ls !! 1

    start  <- getCurrentTime
    result <- evaluate (lcs a b)
    end    <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
    print result
    hPutStrLn stderr $ show ms