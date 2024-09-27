#include <Graphics.hpp>
#include <vector>
#include <iostream>

class ConwayGame {
private:
    std::vector<std::vector<bool>> grid;
    int size;
    int cellSize;
    sf::RenderWindow window;
    sf::Font font;
    sf::Text generationText;
    int generation;

public:
    ConwayGame(int n, int cellSz) : size(n), cellSize(cellSz), generation(0) {
        grid.resize(size, std::vector<bool>(size, false));
        window.create(sf::VideoMode(size * cellSize, size * cellSize + 30), "Conway's Game of Life");
        
        if (!font.loadFromFile("arial.ttf")) {
            std::cout << "Error loading font" << std::endl;
        }
        
        generationText.setFont(font);
        generationText.setCharacterSize(20);
        generationText.setFillColor(sf::Color::White);
        generationText.setPosition(10, size * cellSize);
    }

    void setCell(int row, int col, bool state) {
        if (row >= 0 && row < size && col >= 0 && col < size) {
            grid[row][col] = state;
        }
    }

    int countNeighbors(int row, int col) {
        int count = 0;
        for (int i = -1; i <= 1; i++) {
            for (int j = -1; j <= 1; j++) {
                if (i == 0 && j == 0) continue;
                int newRow = (row + i + size) % size;
                int newCol = (col + j + size) % size;
                count += grid[newRow][newCol] ? 1 : 0;
            }
        }
        return count;
    }

    void update() {
        std::vector<std::vector<bool>> newGrid = grid;
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                int neighbors = countNeighbors(i, j);
                if (grid[i][j]) {
                    newGrid[i][j] = (neighbors == 2 || neighbors == 3);
                } else {
                    newGrid[i][j] = (neighbors == 3);
                }
            }
        }
        grid = newGrid;
        generation++;
    }

    void draw() {
        window.clear(sf::Color::Black);
        
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                sf::RectangleShape cell(sf::Vector2f(cellSize - 1, cellSize - 1));
                cell.setPosition(j * cellSize, i * cellSize);
                cell.setFillColor(grid[i][j] ? sf::Color::White : sf::Color::Black);
                window.draw(cell);
            }
        }
        
        generationText.setString("Generation: " + std::to_string(generation));
        window.draw(generationText);
        
        window.display();
    }

    void run() {
        sf::Clock clock;
        while (window.isOpen()) {
            sf::Event event;
            while (window.pollEvent(event)) {
                if (event.type == sf::Event::Closed)
                    window.close();
                
                if (event.type == sf::Event::MouseButtonPressed) {
                    if (event.mouseButton.button == sf::Mouse::Left) {
                        int col = event.mouseButton.x / cellSize;
                        int row = event.mouseButton.y / cellSize;
                        setCell(row, col, !grid[row][col]);
                    }
                }
            }

            if (clock.getElapsedTime().asMilliseconds() > 100) {
                update();
                clock.restart();
            }

            draw();
        }
    }
};

int main() {
    int size = 50;
    int cellSize = 10;

    ConwayGame game(size, cellSize);

    // Set up initial pattern (e.g., a glider)
    game.setCell(1, 2, true);
    game.setCell(2, 3, true);
    game.setCell(3, 1, true);
    game.setCell(3, 2, true);
    game.setCell(3, 3, true);

    game.run();

    return 0;
}