import { Button } from '@/components/ui/button';

const Home = () => (
    <div>
        <h1>Home</h1>
        <div>
            <input type="text" placeholder="Type a message..." />
            <Button>Send</Button>
        </div>
        <div className="grid auto-rows-min gap-4 md:grid-cols-3">
            <div className="aspect-video rounded-xl bg-muted/50"> <p className="p-4" >Hallo Welt!</p> </div>
            <div className="aspect-video rounded-xl bg-muted/50" />
            <div className="aspect-video rounded-xl bg-muted/50" />
        </div>
    </div>
);

export default Home;