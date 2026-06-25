import Data.Array.Unboxed
import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

knapsack :: Int -> [(Int,Int)] -> Int
knapsack cap items =
    let n   = length items
        arr = listArray (1,n) items :: Array Int (Int,Int)
        dp  = array ((0,0),(n,cap))
                    [((i,w), cell i w) | i <- [0..n], w <- [0..cap]]
        cell 0 _ = 0
        cell i w =
            let (wi, vi) = arr ! i
                skip     = dp ! (i-1, w)
            in if wi > w then skip
               else max skip (dp ! (i-1, w-wi) + vi)
    in dp ! (n, cap)

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let ls      = lines contents
        first   = words (head ls)
        cap     = read (head first)  :: Int
        n       = read (first !! 1)  :: Int
        items   = map (\l -> let [w,v] = map read (words l)
                              in (w,v)) (take n (tail ls)) :: [(Int,Int)]

    start  <- getCurrentTime
    result <- evaluate (knapsack cap items)
    end    <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
    print result
    hPutStrLn stderr $ show ms