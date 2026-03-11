"""Генерация картинок-ассетов при первом запуске."""

from pathlib import Path

def ensure_assets(base_path: Path) -> Path:
    """Создаёт папку assets и генерирует картинки, если их нет."""
    assets_dir = base_path / "assets"
    assets_dir.mkdir(exist_ok=True)

    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return assets_dir

    # Логотип — круглая иконка с буквами TT
    logo_path = assets_dir / "logo.png"
    if not logo_path.exists():
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.ellipse([2, 2, 62, 62], fill="#6366f1", outline="#818cf8", width=3)
        try:
            from PIL import ImageFont
            import os
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
            ]
            font = None
            for fp in font_paths:
                if os.path.exists(fp):
                    font = ImageFont.truetype(fp, 24)
                    break
        except Exception:
            font = None
        d.text((16, 20), "TT", fill="white", font=font)
        img.save(logo_path)

    # Иконка клавиатуры — стилизованная клавиша
    key_path = assets_dir / "keyboard.png"
    if not key_path.exists():
        img = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([4, 4, 44, 44], radius=8, fill="#818cf8", outline="#6366f1", width=2)
        d.ellipse([14, 14, 34, 34], fill="#6366f1")
        img.save(key_path)

    # Декоративная картинка — рука на клавиатуре (схематично)
    hand_path = assets_dir / "hands.png"
    if not hand_path.exists():
        img = Image.new("RGBA", (120, 80), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # Схематичные "пальцы" — круги
        colors = ["#fbbf24", "#22c55e", "#6366f1", "#ec4899", "#ef4444"]
        for i, (x, y) in enumerate([(10, 20), (25, 15), (40, 20), (55, 25), (70, 30)]):
            d.ellipse([x, y, x + 18, y + 18], fill=colors[i % 5], outline="#1e1b4b")
        for i, (x, y) in enumerate([(50, 45), (65, 40), (80, 45), (95, 50), (110, 55)]):
            d.ellipse([x, y, x + 18, y + 18], fill=colors[(i + 2) % 5], outline="#1e1b4b")
        img.save(hand_path)

    return assets_dir
