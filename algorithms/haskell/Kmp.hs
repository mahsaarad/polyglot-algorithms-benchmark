import Data.Array
import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

buildLPS :: String -> Array Int Int
buildLPS pat =
    let m   = length pat
        p   = listArray (0, m-1) pat
        lps = array (0, m-1) $ go 0 1 []
    in lps
  where
    go len i acc
        | i >= length pat = acc
        | pat !! i == pat !! len =
            let len' = len + 1
            in go len' (i+1) ((i, len') : acc)
        | len > 0 = go (buildLPS pat ! (len-1)) i acc
        | otherwise = go 0 (i+1) ((i, 0) : acc)

kmp :: String -> String -> [Int]
kmp text pat
    | null pat = []
    | otherwise =
        let n   = length text
            m   = length pat
            t   = listArray (0, n-1) text
            p   = listArray (0, m-1) pat
            lps = buildLPS pat
        in go t p lps n m 0 0 []
  where
    go t p lps n m i j acc
        | i >= n = reverse acc
        | t ! i == p ! j =
            let i' = i+1; j' = j+1
            in if j' == m
               then go t p lps n m i' (lps ! (j'-1)) ((i'-j') : acc)
               else go t p lps n m i' j' acc
        | j > 0  = go t p lps n m i (lps ! (j-1)) acc
        | otherwise = go t p lps n m (i+1) 0 acc

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let ls  = lines contents
        text = head ls
        pat  = ls !! 1

    start   <- getCurrentTime
    matches <- evaluate (kmp text pat)
    end     <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
    print (length matches)
    if null matches
        then putStrLn ""
        else putStrLn $ unwords (map show matches)
    hPutStrLn stderr $ show ms