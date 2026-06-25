import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

interface Game {
  id: number;
  title: string;
  price: number;
  available: boolean;
}

@Component({
  selector: 'app-game-list',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './game-list.html',
  styleUrl: './game-list.css'
})
export class GameList {

  games: Game[] = [
    {
      id: 1,
      title: 'Half-Life 3',
      price: 29.99,
      available: true
    },
    {
      id: 2,
      title: 'Cyberpunk 2077',
      price: 49.99,
      available: true
    },
    {
      id: 3,
      title: 'Portal 3',
      price: 19.99,
      available: true
    }
  ];

  newGameTitle = '';
  newGamePrice = 0;

  addGame() {

    if (!this.newGameTitle.trim()) {
      return;
    }

    this.games.push({
      id: this.games.length + 1,
      title: this.newGameTitle,
      price: this.newGamePrice,
      available: true
    });

    this.newGameTitle = '';
    this.newGamePrice = 0;
  }

  toggleAvailability(id: number) {

    const game = this.games.find(g => g.id === id);

    if (game) {
      game.available = !game.available;
    }
  }
}