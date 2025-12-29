# Git Tutorial Book - AI Agent Instructions

## Project Overview
This is a Chinese Git tutorial documentation project using Docsify. Individual chapters are in `docs/` directory, concatenated into `book.md` via `build_book.py`.

## Architecture
- **Web Site**: Docsify-powered documentation at `docs/index.html`
- **Book Generation**: Python script concatenates `docs/*.md` files into single `book.md`
- **Navigation**: `docs/_sidebar.md` defines chapter structure
- **Assets**: Images in `docs/assets/` and `assets/` (root level)

## Key Workflows

### Building the Book
```bash
python build_book.py
```
- Concatenates files in order: README.md → docs/00-HOW-TO.md → docs/01-第一部分.md → etc.
- Fixes cross-file links to document-internal anchors
- Promotes headings (H2→H1, H3→H2, etc.) except for H1
- Adjusts image paths to `docs/assets/`
- Output: `book.md` (gitignored, regenerated on build)

### Local Preview
```bash
cd docs
docsify serve
# Or from root: docsify serve docs
```
Serves at http://localhost:3000

### Content Editing
- Edit individual `.md` files in `docs/` directory
- Use Chinese content with gaming metaphors (e.g., "新手村", "副本", "任务系统")
- Maintain mermaid diagrams for flowcharts
- Follow existing anchor naming: `#{chapter}{section}-{chinese-title}`

## Conventions & Patterns

### File Structure
```
docs/
├── index.html          # Docsify config
├── _sidebar.md         # Navigation
├── 00-HOW-TO.md       # Quick start scenarios
├── 01-第一部分.md      # Git basics
├── 02-第二部分.md      # Remote repos & Gitea
├── 03-第三部分.md      # Git Flow collaboration
├── 04-第四部分.md      # Team standards
├── 05-第五部分.md      # Advanced techniques
├── 06-附录.md          # Appendices
├── 07-结语.md          # Conclusion
└── assets/            # Images
```

### Link Patterns
- Cross-file links: `[text](docs/filename.md#_anchor)`
- Build script converts to: `[text](#_anchor)`
- External links preserved as-is

### Commit Message Style
Follow conventional commits adapted for Chinese context:
- `feat: 添加新功能`
- `fix: 修复bug`
- `docs: 更新文档`
- `style: 格式调整`

### Branch Naming
- `feature/功能名` for new features
- `hotfix/问题描述` for urgent fixes
- `release/v1.0.0` for releases

## Dependencies
- **Python 3**: For `build_book.py`
- **Node.js + docsify-cli**: For local preview (`npm install -g docsify-cli`)
- **Git**: Version control with Gitea integration

## Common Tasks
- **Add new chapter**: Create `docs/XX-new-chapter.md`, update `DOCS_ORDER` in `build_book.py`, update `_sidebar.md`
- **Update navigation**: Edit `docs/_sidebar.md` with new section links
- **Fix broken links**: Run build script to regenerate `book.md` with corrected anchors
- **Add images**: Place in `docs/assets/`, reference as `docs/assets/filename.png`

## Quality Checks
- Ensure `book.md` is gitignored (regenerated content)
- Test local preview with `docsify serve docs`
- Verify anchor links work in generated `book.md`
- Check Chinese text encoding (UTF-8)</content>
<parameter name="filePath">c:\Users\80695\Sync\01_当前\10\20251103基于Gitea的代码版本管理与多人协作\.github\copilot-instructions.md