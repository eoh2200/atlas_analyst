# Atlas Analyst

## Usage

Run the script with a county name and project type:

```bash
python cli.py --county "Miami-Dade, FL" --project_type decks
```

The script will create a CSV file in the `output/` directory with contractor information.

**Project Type Options:**
- `decks`
- `sheds`
- `fencing`
- `greenhouses`
- `formwork`
- `general`

## API Key

You need to include your OpenAI API key in a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

