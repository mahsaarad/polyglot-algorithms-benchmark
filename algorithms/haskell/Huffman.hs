import qualified Data.Map.Strict as Map
import Data.List (sortBy, foldl')
import Data.Ord  (comparing)
import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

data Tree = Leaf Int Char | Branch Int Tree Tree

freq :: Tree -> Int
freq (Leaf f _)     = f
freq (Branch f _ _) = f

buildTree :: [(Char,Int)] -> Tree
buildTree freqs =
    let nodes = sortBy (comparing freq) [Leaf f c | (c,f) <- freqs]
    in go nodes
  where
    go [t]    = t
    go (a:b:rest) =
        let merged = Branch (freq a + freq b) a b
            rest'  = insertSorted merged rest
        in go rest'
    go [] = error "empty"
    insertSorted x [] = [x]
    insertSorted x (y:ys)
        | freq x <= freq y = x : y : ys
        | otherwise        = y : insertSorted x ys

codeLengths :: Tree -> Map.Map Char Int
codeLengths tree = go tree 0 Map.empty
  where
    go (Leaf _ c)     d m = Map.insert c (max 1 d) m
    go (Branch _ l r) d m = go r (d+1) (go l (d+1) m)

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    text <- fmap (head . lines) getContents
    let n     = length text
        fmap' = foldl' (\m c -> Map.insertWith (+) c 1 m) Map.empty text
        freqs = Map.toList fmap'

    start  <- getCurrentTime
    let tree    = buildTree freqs
        cl      = codeLengths tree
        total   = sum [f * Map.findWithDefault 1 c cl | (c,f) <- freqs]
        unique  = length freqs
        ratio   = fromIntegral total / (8.0 * fromIntegral n) :: Double
    result <- evaluate (unique, total, ratio)
    end    <- getCurrentTime

    let ms = realToFrac (diffUTCTime end start) * 1000 :: Double
        (u, t, r) = result
    putStrLn $ show u
    putStrLn $ show t
    putStrLn $ show (fromIntegral (round (r * 100)) / 100.0 :: Double)
    hPutStrLn stderr $ show mss