# Create Skill

Create a new Claude Code skill (custom slash command) based on the user's description.

## Arguments

`$ARGUMENTS` — name and/or description of the skill to create, e.g. `my-skill: does X when Y`.

## Instructions

1. Parse `$ARGUMENTS` to extract:
   - **Skill name**: kebab-case identifier (used as the filename and slash command, e.g. `my-skill` → `/my-skill`)
   - **Skill description**: what the skill should do and when to trigger it

   If the name or description is unclear, ask the user one focused question before proceeding.

2. Determine the correct location:
   - **Project-level** (default): `.claude/commands/<skill-name>.md` — available only inside this repo
   - **User-level**: `~/.claude/commands/<skill-name>.md` — available in all projects
   
   Ask the user which scope they want if they haven't specified.

3. Create the skill file using this template:

```
# <Skill Title>

<One-sentence description of what the skill does and when to use it.>

## Arguments

`$ARGUMENTS` — <describe expected input, or write "No arguments expected." if none>

## Instructions

<Step-by-step instructions for Claude to follow when this skill is invoked.
Be specific: name files to read/edit, tools to use, and conditions to check.
End with a clear success condition.>
```

4. Write the file to the chosen location using the Write tool.

5. Confirm to the user:
   - The full path of the created file
   - The slash command they can now use (e.g. `/my-skill`)
   - A one-line summary of what it does
   - Remind them to reload Claude Code if the skill doesn't appear immediately (`/reload` or restart the session)

## Notes

- Skill names must be kebab-case (lowercase, hyphens only, no spaces).
- Keep instructions declarative and precise — Claude executes them literally.
- Use `$ARGUMENTS` anywhere in the file to inject the user's input at invocation time.
- Avoid vague verbs like "handle" or "process" — prefer "read", "edit", "run", "write", "search".
