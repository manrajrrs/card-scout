from mcp.server.mcpserver import MCPServer

from identify import identify_card

mcp = MCPServer("card-scout")


@mcp.tool()
def identify_card_from_photo(image_path: str) -> dict:
    """Identify a Riftbound card from a photo.

    Returns the card's name, set_code, number and rarity.
    Give the full file path to a JPG photo of a single card.
    """
    with open(image_path, "rb") as f:
        return identify_card(f.read())


if __name__ == "__main__":
    mcp.run(transport="stdio")