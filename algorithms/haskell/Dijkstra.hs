import qualified Data.Map.Strict as Map
import qualified Data.Set        as Set
import Data.Time.Clock
import System.IO
import Control.Exception (evaluate)

type Graph = Map.Map Int [(Int, Int)]

dijkstra :: Graph -> Int -> Int -> Map.Map Int Int
dijkstra graph v src =
    let inf   = maxBound `div` 2
        nodes = [0..v-1]
        dist0 = Map.fromList [(n, if n == src then 0 else inf) | n <- nodes]
        pq0   = Set.singleton (0, src)
    in go graph dist0 pq0
  where
    go g dist pq
        | Set.null pq = dist
        | otherwise   =
            let ((d, u), pq') = Set.deleteFindMin pq
                neighbors     = Map.findWithDefault [] u g
                (dist', pq'') = foldr (relax d) (dist, pq') neighbors
            in if d > Map.findWithDefault maxBound u dist
               then go g dist pq'
               else go g dist' pq''

    relax d (to, w) (dist, pq) =
        let nd  = d + w
            old = Map.findWithDefault maxBound to dist
        in if nd < old
           then (Map.insert to nd dist, Set.insert (nd, to) pq)
           else (dist, pq)

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    contents <- getContents
    let ls        = lines contents
        firstLine = words (head ls)
        v         = read (firstLine !! 0) :: Int
        _e        = read (firstLine !! 1) :: Int
        src       = read (firstLine !! 2) :: Int
        edgeLines = tail ls
        parseEdge l = let [u,t,w] = map read (words l) in (u, t, w)
        edgeList  = map parseEdge (filter (not . null) edgeLines)
        graph     = foldr (\(u,t,w) g ->
                        Map.insertWith (++) u [(t,w)] g)
                    Map.empty edgeList

    start  <- getCurrentTime
    result <- evaluate (dijkstra graph v src)
    end    <- getCurrentTime

    let ms   = realToFrac (diffUTCTime end start) * 1000 :: Double
        dists = [Map.findWithDefault (-1) i result | i <- [0..v-1]]
    putStrLn $ unwords (map show dists)
    hPutStrLn stderr $ show ms