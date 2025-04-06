
import { useGameContext } from "@/context/GameContext";
import { Coins, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import PlayerProfile from "./PlayerProfile";

const GameHeader = () => {
  const { gameState } = useGameContext();
  
  return (
    <div className="fixed top-0 inset-x-0 z-10 bg-gradient-to-b from-background/80 to-background/0 backdrop-blur-sm py-2">
      <div className="container mx-auto flex justify-between items-center px-4">
        <div className="flex items-center space-x-2">
          <Coins className="w-5 h-5 text-yellow-500" />
          <div className="font-semibold">
            {Math.floor(gameState.player.balance).toLocaleString()}
          </div>
        </div>
        
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="rounded-full">
              <User className="w-5 h-5" />
            </Button>
          </SheetTrigger>
          <SheetContent className="w-[85vw] sm:max-w-md">
            <SheetHeader>
              <SheetTitle>Player Profile</SheetTitle>
            </SheetHeader>
            <PlayerProfile />
          </SheetContent>
        </Sheet>
      </div>
    </div>
  );
};

export default GameHeader;
