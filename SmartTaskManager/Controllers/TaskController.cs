using Microsoft.AspNetCore.Mvc;

namespace SmartTaskManager.Controllers;

public class TaskController : Controller
{
    private readonly TaskService _service;

    public TaskController(TaskService service)
    {
        _service = service;
    }

    public async Task<IActionResult> Index()
    {
        var tasks = await _service.GetAllTasks();
        return View(tasks);
    }

    public IActionResult Create()
    {
        return View();
    }

    [HttpPost]
    public async Task<IActionResult> Create(TaskItem task)
    {
        await _service.CreateTask(task);
        return RedirectToAction("Index");
    }
}