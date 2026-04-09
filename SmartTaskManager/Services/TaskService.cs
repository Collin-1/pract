using Microsoft.EntityFrameworkCore;

public class TaskService
{
    private readonly AppDbContext _context;

    public TaskService(AppDbContext context)
    {
        _context = context;
    }

    public async Task<List<TaskItem>> GetAllTasks()
    {
        return await _context.Tasks.ToListAsync();
    }

    public async Task<TaskItem> CreateTask(TaskItem task)
    {
        _context.Tasks.Add(task);
        await _context.SaveChangesAsync();
        return task;   
    }
}

