using Microsoft.AspNetCore.Mvc;

namespace SmartTaskManager.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TaskApiController : ControllerBase
{
    private readonly TaskService _service;

    public TaskApiController(TaskService service)
    {
        _service = service;
    }

    [HttpGet]
    public async Task<IActionResult> GetTasks()
    {
        return Ok(await _service.GetAllTasks());
    }
}